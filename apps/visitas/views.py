# apps/visitas/views.py

from datetime import date, datetime, timedelta
import json
from types import SimpleNamespace

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import transaction
from django.db.models import (
    Count, Avg, DurationField, ExpressionWrapper, F,
    OuterRef, Subquery, Exists, Value, CharField,
    IntegerField, BooleanField, DateTimeField, Case, When,
)
from django.db.models.functions import ExtractIsoWeekDay, TruncWeek, Coalesce
from django.contrib.auth import get_user_model

from apps.visitas.models import Visita, DetalleVisita, ProductoPresentado
from apps.productos.models import Producto
from apps.rutas.models import Ruta
from apps.doctores.models import Doctor

from .draft import (
    get_draft,
    save_draft,
    new_draft,
    clear_draft,
    get_ruta_id,
)

# ---------------------------------------------------------
# 1. INICIAR VISITA
# ---------------------------------------------------------
@login_required
def iniciar_visita(request, ruta_id=None, doctor_id=None):
    """
    Ya no muestra un template propio.
    - Resuelve doctor/ruta.
    - Crea (o reutiliza) un borrador de visita.
    - Redirige a la pantalla unificada 'agregar_productos'
      (visita_en_curso).
    """
    user = request.user

    ruta = None
    doctor = None

    # Resolver doctor/ruta con las mismas reglas actuales
    if ruta_id:
        ruta = get_object_or_404(Ruta, id=ruta_id, usuario=user)
        doctor = ruta.doctor
    elif doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)
        # Validación de permisos para visitadores
        if not (user.is_superuser or getattr(user, "rol", "") == "supervisor"):
            if getattr(doctor, "visitador_id", None) != user.id:
                messages.error(request, "No tienes permiso para visitar a este doctor.")
                return redirect("visitas:gestionar_visitas_medicas")
    else:
        return redirect("visitas:gestionar_visitas_medicas")

    # ¿Ya hay un draft activo?
    draft = get_draft(request)

    # Si ya existe un borrador para este mismo doctor, lo reutilizamos
    if draft and draft.get("doctor_id") == doctor.id:
        return redirect("visitas:agregar_productos")

    # Si no hay draft o es de otro doctor, creamos uno nuevo
    draft = new_draft(
        usuario_id=user.id,
        doctor_id=doctor.id,
        ruta_id=(ruta.id if ruta else None),
        ubicacion_inicio="",  # la ubicación se capturará en la plantilla unificada
        origen="rutas" if ruta_id else "buscador",
    )
    save_draft(request, draft)
    messages.info(request, "Visita iniciada. Complete los datos de la visita.")

    return redirect("visitas:agregar_productos")


# ---------------------------------------------------------
# 2. VISITA EN CURSO (pantalla única)
# ---------------------------------------------------------
@login_required
def agregar_productos(request):
    """
    Lista estándar en el borrador:
    draft["items"] = [
        {"producto_id": int, "cantidad": int},
        ...
    ]
    """
    draft = get_draft(request)

    if not draft:
        messages.error(request, "No se ha iniciado una visita.")
        return redirect("visitas:gestionar_visitas_medicas")

    doctor_id = draft.get("doctor_id")
    if not doctor_id:
        messages.error(request, "El borrador no tiene un médico asociado.")
        return redirect("visitas:gestionar_visitas_medicas")

    doctor = get_object_or_404(Doctor, id=doctor_id)

    ruta = None
    ruta_id = draft.get("ruta_id")
    if ruta_id:
        ruta = Ruta.objects.filter(id=ruta_id).select_related("doctor").first()

    # Lista unificada de items: [{producto_id, cantidad}]
    items = draft.get("items", [])
    comentarios = draft.get("comentarios", "")

    # ----------------- FILTRO POR TIPO DE PRODUCTO -----------------
    filtro_tipo = (request.GET.get("tipo") or "todos").strip()
    productos_qs = Producto.objects.all().order_by("nombre")
    if filtro_tipo in {"prescribible", "muestra", "promocional", "merch"}:
        productos_qs = productos_qs.filter(tipo_producto=filtro_tipo)

    # Para enriquecer los items con nombre/tipo del producto
    producto_ids = [it.get("producto_id") for it in items if it.get("producto_id")]
    productos_map = Producto.objects.in_bulk(producto_ids)

    # ----------------- POST: AGREGAR / QUITAR / GUARDAR / FINALIZAR -----------------
    if request.method == "POST":
        accion = request.POST.get("accion")

        # Comentarios
        comentarios = request.POST.get("comentarios", "").strip()
        draft["comentarios"] = comentarios

        # 🔹 NUEVO: guardar ubicación de inicio si viene del formulario
        ubicacion_inicio_post = request.POST.get("ubicacion_inicio")
        if ubicacion_inicio_post:
            draft["ubicacion_inicio"] = ubicacion_inicio_post

        # Cargar items actuales desde el borrador
        items = draft.get("items", [])

        # Agregar producto
        if accion == "agregar_item":
            try:
                producto_id = int(request.POST.get("producto_id"))
                cantidad = int(request.POST.get("cantidad") or 0)
            except (TypeError, ValueError):
                messages.error(
                    request,
                    "Debes seleccionar un producto y una cantidad válida.",
                )
            else:
                if cantidad <= 0:
                    messages.error(request, "La cantidad debe ser mayor que cero.")
                else:
                    if not Producto.objects.filter(id=producto_id).exists():
                        messages.error(request, "El producto seleccionado no existe.")
                    else:
                        items.append(
                            {
                                "producto_id": producto_id,
                                "cantidad": cantidad,
                            }
                        )
                        messages.success(request, "Producto agregado a la visita.")

            draft["items"] = items
            save_draft(request, draft)
            return redirect("visitas:agregar_productos")

        # Eliminar producto
        elif accion == "eliminar_item":
            try:
                idx = int(request.POST.get("item_index", "-1"))
            except (TypeError, ValueError):
                idx = -1

            if 0 <= idx < len(items):
                items.pop(idx)
                messages.info(request, "Producto eliminado de la visita.")
            else:
                messages.error(
                    request,
                    "No se pudo identificar el producto a eliminar.",
                )

            draft["items"] = items
            save_draft(request, draft)
            return redirect("visitas:agregar_productos")

        # Solo guardar borrador
        elif accion == "guardar":
            draft["items"] = items
            save_draft(request, draft)
            messages.success(
                request,
                "Cambios guardados en el borrador de la visita.",
            )
            return redirect("visitas:agregar_productos")

        # Finalizar visita
        elif accion == "finalizar":
            draft["items"] = items
            save_draft(request, draft)
            return redirect("visitas:finalizar_visita")

        # Cancelar visita
        elif accion == "cancelar":
            def _post_commit():
                clear_draft(request)
                messages.info(request, "La visita fue cancelada.")

            transaction.on_commit(_post_commit)
            return redirect("visitas:gestionar_visitas_medicas")

    # ----------------- PREPARAR ITEMS ENRIQUECIDOS PARA EL TEMPLATE -----------------
    items_enriquecidos = []
    for idx, it in enumerate(items):
        prod = productos_map.get(it.get("producto_id"))
        if not prod:
            continue
        items_enriquecidos.append(
            {
                "index": idx,
                "producto_id": prod.id,
                "producto_nombre": prod.nombre,
                "tipo_producto": prod.get_tipo_producto_display(),
                "cantidad": it.get("cantidad", 0),
            }
        )

    context = {
        "doctor": doctor,
        "ruta": ruta,
        "draft": draft,
        "comentarios": comentarios,
        "items": items_enriquecidos,
        "productos": productos_qs,
        "filtro_tipo": filtro_tipo,
    }
    return render(request, "visitas/visita_en_curso.html", context)

# ---------------------------------------------------------
# 3. GESTIONAR VISITAS MÉDICAS
# ---------------------------------------------------------
@login_required
def gestionar_visitas_medicas(request):
    user = request.user
    hoy = timezone.localdate()

    # 1) Rutas del visitador (todas desde hoy hacia adelante o recientes)
    rutas = (
        Ruta.objects.filter(usuario=user)
        .select_related("doctor")
        .annotate(
            # 🟢 Ruta cubierta = existe visita asociada (finalizada)
            cubierta=Exists(
                Visita.objects.filter(
                    ruta_id=OuterRef("pk"), fecha_final__isnull=False
                )
            )
        )
        .order_by("fecha_visita")
    )

    # 2) Doctores asignados al visitador
    doctores_base = Doctor.objects.filter(visitador_id=user.id)

    # Límites del mes actual
    first_month_day = hoy.replace(day=1)
    next_month = (first_month_day.replace(day=28) + timedelta(days=4)).replace(day=1)

    # Visitas finalizadas por doctor (conteo en el mes)
    visitas_count_sq = (
        Visita.objects.filter(
            usuario=user,
            doctor_id=OuterRef("pk"),
            fecha_inicio__gte=first_month_day,
            fecha_inicio__lt=next_month,
            fecha_final__isnull=False,
        )
        .values("doctor_id")
        .annotate(c=Count("id"))
        .values("c")[:1]
    )

    # Última visita finalizada por doctor
    ultima_visita_sq = (
        Visita.objects.filter(
            usuario=user, doctor_id=OuterRef("pk"), fecha_final__isnull=False
        )
        .order_by("-fecha_inicio")
        .values("fecha_inicio")[:1]
    )

    # ¿Tiene ruta futura?
    ruta_futura_exists = Exists(
        Ruta.objects.filter(
            usuario=user,
            doctor_id=OuterRef("pk"),
            fecha_visita__gte=hoy,
        )
    )

    # Id de próxima ruta (para el botón "Iniciar")
    ruta_proxima_id_sq = (
        Ruta.objects.filter(
            usuario=user,
            doctor_id=OuterRef("pk"),
            fecha_visita__gte=hoy,
        )
        .order_by("fecha_visita")
        .values("id")[:1]
    )

    doctores_qs = (
        doctores_base.annotate(
            visitas_mes=Coalesce(
                Subquery(visitas_count_sq, output_field=IntegerField()), Value(0)
            ),
            ultima_visita=Subquery(
                ultima_visita_sq, output_field=DateTimeField()
            ),
            tiene_ruta=ruta_futura_exists,
            ruta_proxima_id=Subquery(
                ruta_proxima_id_sq, output_field=IntegerField()
            ),
        )
        .annotate(
            # Semáforo & label del estado
            semaforo=Case(
                When(visitas_mes__gt=0, then=Value("verde")),
                When(tiene_ruta=True, then=Value("amarillo")),
                default=Value("rojo"),
                output_field=CharField(),
            ),
            estado_label=Case(
                When(visitas_mes__gt=0, then=Value("Cubierto")),
                When(tiene_ruta=True, then=Value("Planificado")),
                default=Value("Pendiente"),
                output_field=CharField(),
            ),
        )
        .order_by("apellido", "nombre")
    )

    # Añade atributo .ruta_disponible con .id si existe
    doctores = []
    for d in doctores_qs:
        setattr(
            d,
            "ruta_disponible",
            SimpleNamespace(id=d.ruta_proxima_id) if d.ruta_proxima_id else None,
        )
        doctores.append(d)

    return render(
        request,
        "visitas/gestionar_visitas_medicas.html",
        {
            "rutas": rutas,
            "doctores": doctores,
        },
    )


# ---------------------------------------------------------
# 4. FINALIZAR / CANCELAR VISITA
# ---------------------------------------------------------
@login_required
def finalizar_visita(request):
    """
    Crea la Visita real y sus DetalleVisita a partir del borrador.
    Usa la lista unificada 'items' (producto_id + cantidad).
    """
    draft = get_draft(request)
    if not draft:
        messages.error(request, "No hay borrador para finalizar.")
        return redirect("visitas:gestionar_visitas_medicas")

    doctor_id = draft.get("doctor_id")
    if not doctor_id:
        messages.error(request, "Borrador inválido: falta doctor.")
        return redirect("visitas:agregar_productos")

    items = draft.get("items", [])

    # 🔹 Normalizar fecha_inicio desde el borrador (evita errores de tipo)
    fecha_inicio_raw = draft.get("fecha_inicio_iso")
    fecha_inicio = None
    if fecha_inicio_raw:
        try:
            fecha_inicio = parse_datetime(fecha_inicio_raw)
        except Exception:
            fecha_inicio = None

    if fecha_inicio is None:
        fecha_inicio = timezone.now()

    # 🔹 Obtener ruta_id usando el helper (considera ruta y ruta_sugerida)
    ruta_id = get_ruta_id(request)

    try:
        with transaction.atomic():
            # 1) Crear la visita
            visita = Visita.objects.create(
                usuario=request.user,
                doctor_id=doctor_id,
                ruta_id=ruta_id,
                fecha_inicio=fecha_inicio,
                ubicacion_inicio=draft.get("ubicacion_inicio") or "",
                comentarios=draft.get("comentarios") or "",
                fecha_final=timezone.now(),
            )

            # 2) Calcular duración si tu modelo lo soporta
            if hasattr(visita, "calcular_duracion"):
                try:
                    visita.duracion = visita.calcular_duracion()
                    visita.save(update_fields=["duracion"])
                except Exception:
                    pass

            # 3) Crear detalles de visita a partir de items
            producto_ids = [
                it.get("producto_id") for it in items if it.get("producto_id")
            ]
            productos_map = Producto.objects.in_bulk(producto_ids)

            detalles = []
            for it in items:
                producto_id = it.get("producto_id")
                cantidad = it.get("cantidad") or 0

                if not producto_id or cantidad <= 0:
                    continue

                prod = productos_map.get(producto_id)
                if not prod:
                    continue

                # Tipo de entrega (solo aplica para muestras/merch)
                tipo_entrega = None
                if prod.tipo_producto in {"muestra", "merch"}:
                    tipo_entrega = prod.tipo_producto

                detalles.append(
                    DetalleVisita(
                        visita=visita,
                        producto_id=producto_id,
                        cantidad=cantidad,
                        tipo_entrega=tipo_entrega,
                    )
                )

            if detalles:
                DetalleVisita.objects.bulk_create(detalles)

            # 4) Actualizar ruta asociada (si la hay)
            try:
                if ruta_id:
                    ruta = Ruta.objects.filter(id=ruta_id).first()
                    if ruta:
                        # Usar la lógica centralizada del modelo
                        ruta.actualizar_estatus()
            except Exception:
                # No romper el cierre por un problema con rutas
                pass

    except Exception as ex:
        messages.error(request, f"No se pudo finalizar la visita: {ex}")
        return redirect("visitas:agregar_productos")

    # 5) Limpiar borrador y redirigir
    def _post_commit():
        clear_draft(request)
        messages.success(
            request, "Visita finalizada y ruta marcada como completada."
        )

    transaction.on_commit(_post_commit)
    return redirect("visitas:gestionar_visitas_medicas")


@login_required
def cancelar_visita(request):
    def _post_commit():
        clear_draft(request)
        messages.info(request, "La visita fue cancelada.")

    transaction.on_commit(_post_commit)
    return redirect("visitas:gestionar_visitas_medicas")

# ---------------------------------------------------------
# 5. HISTORIAL
# ---------------------------------------------------------
@login_required
def ver_historial(request):
    """
    Muestra el historial completo de visitas, entregas y productos presentados.
    Compatible con el nuevo flujo: solo cuenta visitas finalizadas (fecha_final no nula).
    """
    from django.db.models import (
        Count,
        Avg,
        DurationField,
        ExpressionWrapper,
        F,
        Value,
        Case,
        When,
        IntegerField,
        Exists,
        OuterRef,
        Subquery,
        BooleanField,
    )
    from django.db.models.functions import ExtractIsoWeekDay, Coalesce
    from datetime import date, datetime, timedelta
    from django.contrib.auth import get_user_model
    import json

    User = get_user_model()
    user = request.user
    is_supervisor = user.is_superuser or getattr(user, "rol", "") == "supervisor"

    # ==== Determinar usuario objetivo ====
    rep_id = request.GET.get("rep_id")
    usuario_target = user
    visitadores_qs = User.objects.none()

    if is_supervisor:
        visitadores_qs = User.objects.filter(rol="visitador").order_by(
            "first_name", "last_name"
        )
        if rep_id:
            usuario_target = get_object_or_404(User, id=rep_id, rol="visitador")

    # ==== Parámetros de semana ====
    hoy = timezone.localdate()
    y, w, _ = hoy.isocalendar()
    semana = int(request.GET.get("semana", w))
    año = int(request.GET.get("año", y))

    weekpick = request.GET.get("weekpick")
    if weekpick:
        try:
            a, ws = weekpick.split("-W")
            año = int(a)
            semana = int(ws)
        except Exception:
            pass

    week_start = datetime.fromisocalendar(año, semana, 1).date()
    week_end = week_start + timedelta(days=6)

    # ==== Visitas finalizadas ====
    visitas_qs = (
        Visita.objects.filter(
            usuario=usuario_target,
            fecha_inicio__date__gte=week_start,
            fecha_inicio__date__lte=week_end,
            fecha_final__isnull=False,
        )
        .annotate(
            duracion_min=ExpressionWrapper(
                F("fecha_final") - F("fecha_inicio"),
                output_field=DurationField(),
            )
        )
        .order_by("-fecha_inicio")
    )

    detalles_qs = DetalleVisita.objects.filter(visita__in=visitas_qs)
    presentados_qs = ProductoPresentado.objects.filter(visita__in=visitas_qs)

    total_visitas_semana = visitas_qs.count()
    total_entregas = detalles_qs.count()
    total_productos_presentados = presentados_qs.count()

    tiempo_promedio = visitas_qs.aggregate(
        prom=Avg(
            ExpressionWrapper(
                F("fecha_final") - F("fecha_inicio"), output_field=DurationField()
            )
        )
    )["prom"] or timedelta(minutes=0)

    # ==== Visitas por día ====
    visitas_por_dia = (
        visitas_qs.annotate(dow=ExtractIsoWeekDay("fecha_inicio"))
        .values("dow")
        .annotate(c=Count("id"))
        .order_by("dow")
    )

    nombres_dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    mapa = {row["dow"]: row["c"] for row in visitas_por_dia}
    visitas_semana_labels = nombres_dias
    visitas_semana_data = [mapa.get(i, 0) for i in range(1, 8)]

    # ==== Top doctores ====
    def _first_token(s: str) -> str:
        s = (s or "").strip()
        return s.split()[0] if s else ""

    top_raw = (
        visitas_qs.values("doctor__apellido", "doctor__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    top_doctores_labels = [
        (
            f"{_first_token(d['doctor__apellido'])} {_first_token(d['doctor__nombre'])}".strip()
            or "Sin nombre"
        )
        for d in top_raw
    ]
    top_doctores_data = [d["total"] for d in top_raw]

    # ==== Navegación semanal ====
    prev_monday = week_start - timedelta(days=7)
    next_monday = week_start + timedelta(days=7)
    prev_year, prev_week, _ = prev_monday.isocalendar()
    next_year, next_week, _ = next_monday.isocalendar()
    weekpick_value = f"{año}-W{semana:02d}"

    # ==== Cobertura mensual ====
    month_param = request.GET.get("month")
    if month_param:
        try:
            y_, m_ = month_param.split("-")
            year_q = int(y_)
            month_q = int(m_)
        except Exception:
            year_q, month_q = hoy.year, hoy.month
    else:
        year_q, month_q = hoy.year, hoy.month

    month_value = f"{year_q}-{month_q:02d}"
    first_month_day = date(year_q, month_q, 1)
    next_month = (first_month_day.replace(day=28) + timedelta(days=4)).replace(day=1)
    month_end = next_month - timedelta(days=1)

    doctores_base = Doctor.objects.all()
    if not is_supervisor:
        doctores_base = doctores_base.filter(visitador_id=usuario_target.id)

    visitado_mes_qs = Visita.objects.filter(
        usuario=usuario_target,
        doctor_id=OuterRef("pk"),
        fecha_inicio__gte=first_month_day,
        fecha_inicio__lt=next_month,
        fecha_final__isnull=False,
    )

    visitas_count_sq = (
        Visita.objects.filter(
            usuario=usuario_target,
            doctor_id=OuterRef("pk"),
            fecha_inicio__gte=first_month_day,
            fecha_inicio__lt=next_month,
            fecha_final__isnull=False,
        )
        .values("doctor_id")
        .annotate(c=Count("id"))
        .values("c")[:1]
    )

    doctores = (
        doctores_base.annotate(
            visitas_mes=Coalesce(
                Subquery(visitas_count_sq, output_field=IntegerField()), Value(0)
            ),
            visitado_mes=Exists(visitado_mes_qs),
        )
        .order_by("apellido", "nombre")
    )

    asignados_total = doctores.count()
    visitados_count = sum(1 for d in doctores if d.visitado_mes)
    cobertura_pct = (
        round((visitados_count / asignados_total) * 100, 1)
        if asignados_total
        else 0.0
    )
    pendientes = max(asignados_total - visitados_count, 0)

    # ==== Render ====
    titulo_nombre = (
        "Mi historial"
        if not is_supervisor
        else f"Historial — {usuario_target.get_full_name() or usuario_target.username}"
    )

    return render(
        request,
        "visitas/historial.html",
        {
            "titulo_nombre": titulo_nombre,
            "is_supervisor": is_supervisor,
            "visitadores": visitadores_qs,
            "rep_id": str(rep_id or ""),
            "semana_actual": semana,
            "año_actual": año,
            "semana_anterior": prev_week,
            "año_anterior": prev_year,
            "semana_siguiente": next_week,
            "año_siguiente": next_year,
            "weekpick_value": weekpick_value,
            "month_value": month_value,
            "visitas": visitas_qs,
            "detalles": detalles_qs,
            "presentados": presentados_qs,
            "total_visitas_semana": total_visitas_semana,
            "total_entregas": total_entregas,
            "total_productos_presentados": total_productos_presentados,
            "cobertura_pct": cobertura_pct,
            "visitados_count": visitados_count,
            "pendientes": pendientes,
            "asignados_total": asignados_total,
            "visitas_semana_labels": json.dumps(visitas_semana_labels),
            "visitas_semana_data": json.dumps(visitas_semana_data),
            "cobertura_labels": json.dumps(["Visitados", "Pendientes"]),
            "cobertura_data": json.dumps([visitados_count, pendientes]),
            "top_doctores_labels": json.dumps(top_doctores_labels),
            "top_doctores_data": json.dumps(top_doctores_data),
        },
    )