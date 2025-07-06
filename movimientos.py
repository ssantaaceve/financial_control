from supabase_config import get_supabase_client
from datetime import datetime

def registrar_movimiento_DB(usuario_id, fecha, categoria_nombre, monto, tipo, descripcion):
    """
    Registra un nuevo movimiento en Supabase.
    """
    try:
        supabase = get_supabase_client()
        
        # Primero, obtener o crear la categoría
        categoria_id = obtener_o_crear_categoria(usuario_id, categoria_nombre, tipo)
        
        if not categoria_id:
            print("❌ Error al obtener/crear categoría.")
            return False
        
        # Crear el movimiento
        movimiento_data = {
            "usuario_id": usuario_id,
            "fecha": fecha,
            "categoria_id": categoria_id,
            "monto": monto,
            "tipo": tipo,
            "descripcion": descripcion,
            "es_recurrente": False
        }
        
        response = supabase.table('movimientos').insert(movimiento_data).execute()
        
        if response.data:
            print("✅ Movimiento registrado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al registrar movimiento: {e}")
        return False

def obtener_o_crear_categoria(usuario_id, nombre_categoria, tipo):
    """
    Obtiene una categoría existente o crea una nueva.
    """
    try:
        supabase = get_supabase_client()
        
        # Buscar categoría existente
        response = supabase.table('categorias').select('id').eq('usuario_id', usuario_id).eq('nombre', nombre_categoria).eq('tipo', tipo).execute()
        
        if response.data:
            return response.data[0]['id']
        
        # Crear nueva categoría
        categoria_data = {
            "nombre": nombre_categoria,
            "tipo": tipo,
            "usuario_id": usuario_id
        }
        
        response = supabase.table('categorias').insert(categoria_data).execute()
        
        if response.data:
            return response.data[0]['id']
        
        return None
        
    except Exception as e:
        print(f"❌ Error al obtener/crear categoría: {e}")
        return None

def obtener_resumen_financiero(usuario_id):
    """
    Obtiene el resumen financiero del mes actual.
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener fecha actual y primer día del mes
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        primer_dia_mes = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        
        # Obtener ingresos del mes
        response_ingresos = supabase.table('movimientos').select('monto').eq('usuario_id', usuario_id).eq('tipo', 'Ingreso').gte('fecha', primer_dia_mes).lte('fecha', fecha_actual).execute()
        
        total_ingresos = sum(mov['monto'] for mov in response_ingresos.data) if response_ingresos.data else 0
        
        # Obtener gastos del mes
        response_gastos = supabase.table('movimientos').select('monto').eq('usuario_id', usuario_id).eq('tipo', 'Gasto').gte('fecha', primer_dia_mes).lte('fecha', fecha_actual).execute()
        
        total_gastos = sum(mov['monto'] for mov in response_gastos.data) if response_gastos.data else 0
        
        # Calcular balance
        balance = total_ingresos - total_gastos
        
        return {
            "ingresos": total_ingresos,
            "gastos": total_gastos,
            "balance": balance
        }
        
    except Exception as e:
        print(f"❌ Error al obtener resumen financiero: {e}")
        return None

def registrar_movimiento_recurrente_DB(usuario_id, categoria_nombre, monto, tipo, descripcion, frecuencia, fecha_inicio, fecha_fin):
    """
    Registra un movimiento recurrente en Supabase.
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener o crear categoría
        categoria_id = obtener_o_crear_categoria(usuario_id, categoria_nombre, tipo)
        
        if not categoria_id:
            return False
        
        # Crear movimiento recurrente
        movimiento_data = {
            "usuario_id": usuario_id,
            "fecha": fecha_inicio,
            "categoria_id": categoria_id,
            "monto": monto,
            "tipo": tipo,
            "descripcion": descripcion,
            "es_recurrente": True,
            "frecuencia": frecuencia,
            "fecha_fin": fecha_fin
        }
        
        response = supabase.table('movimientos').insert(movimiento_data).execute()
        
        if response.data:
            print("✅ Movimiento recurrente registrado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al registrar movimiento recurrente: {e}")
        return False

def obtener_movimientos_recurrentes_pendientes(usuario_id):
    """
    Obtiene los movimientos recurrentes pendientes.
    """
    try:
        supabase = get_supabase_client()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        
        response = supabase.table('movimientos').select('*, categorias(nombre)').eq('usuario_id', usuario_id).eq('es_recurrente', True).lte('fecha', fecha_actual).gte('fecha_fin', fecha_actual).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"❌ Error al obtener movimientos recurrentes: {e}")
        return []

def aprobar_movimiento_recurrente(movimiento_id):
    """
    Aprueba un movimiento recurrente.
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener datos del movimiento recurrente
        response = supabase.table('movimientos').select('*').eq('id', movimiento_id).execute()
        
        if not response.data:
            print("❌ Movimiento no encontrado.")
            return False
        
        movimiento = response.data[0]
        
        # Crear movimiento regular
        nuevo_movimiento = {
            "usuario_id": movimiento['usuario_id'],
            "fecha": datetime.now().strftime('%Y-%m-%d'),
            "categoria_id": movimiento['categoria_id'],
            "monto": movimiento['monto'],
            "tipo": movimiento['tipo'],
            "descripcion": movimiento['descripcion'],
            "es_recurrente": False
        }
        
        response = supabase.table('movimientos').insert(nuevo_movimiento).execute()
        
        if response.data:
            print("✅ Movimiento aprobado y registrado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al aprobar movimiento: {e}")
        return False

def rechazar_movimiento_recurrente(movimiento_id):
    """
    Rechaza un movimiento recurrente (lo elimina).
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('movimientos').delete().eq('id', movimiento_id).execute()
        
        if response.data:
            print("✅ Movimiento rechazado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al rechazar movimiento: {e}")
        return False

def obtener_historial_movimientos(usuario_id, filtros=None):
    """
    Obtiene el historial de movimientos con filtros opcionales.
    """
    try:
        supabase = get_supabase_client()
        
        query = supabase.table('movimientos').select('*, categorias(nombre)').eq('usuario_id', usuario_id).eq('es_recurrente', False)
        
        # Aplicar filtros si se proporcionan
        if filtros:
            if filtros.get('tipo'):
                query = query.eq('tipo', filtros['tipo'])
            
            if filtros.get('fecha_inicio'):
                query = query.gte('fecha', filtros['fecha_inicio'])
            
            if filtros.get('fecha_fin'):
                query = query.lte('fecha', filtros['fecha_fin'])
            
            if filtros.get('monto_min'):
                query = query.gte('monto', filtros['monto_min'])
            
            if filtros.get('monto_max'):
                query = query.lte('monto', filtros['monto_max'])
        
        # Ordenar por fecha descendente
        response = query.order('fecha', desc=True).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")
        return []

def obtener_categorias_usuario(usuario_id):
    """
    Obtiene todas las categorías del usuario.
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('categorias').select('nombre, tipo').eq('usuario_id', usuario_id).order('nombre').execute()
        
        return [cat['nombre'] for cat in response.data] if response.data else []
        
    except Exception as e:
        print(f"❌ Error al obtener categorías: {e}")
        return []

def crear_presupuesto(usuario_id, categoria_nombre, monto_maximo, periodo, fecha_inicio, fecha_fin):
    """
    Crea un nuevo presupuesto.
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener categoría (asumimos que ya existe)
        response = supabase.table('categorias').select('id').eq('usuario_id', usuario_id).eq('nombre', categoria_nombre).execute()
        
        if not response.data:
            print("❌ Categoría no encontrada.")
            return False
        
        categoria_id = response.data[0]['id']
        
        # Crear presupuesto
        presupuesto_data = {
            "usuario_id": usuario_id,
            "categoria_id": categoria_id,
            "monto_maximo": monto_maximo,
            "periodo": periodo,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }
        
        response = supabase.table('presupuestos').insert(presupuesto_data).execute()
        
        if response.data:
            print("✅ Presupuesto creado exitosamente.")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error al crear presupuesto: {e}")
        return False

def obtener_presupuestos_usuario(usuario_id):
    """
    Obtiene los presupuestos del usuario.
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('presupuestos').select('*, categorias(nombre)').eq('usuario_id', usuario_id).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"❌ Error al obtener presupuestos: {e}")
        return []

def gasto_acumulado(usuario_id, categoria_nombre, fecha_inicio, fecha_fin):
    """
    Calcula el gasto acumulado en una categoría en un período.
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener categoría
        response = supabase.table('categorias').select('id').eq('usuario_id', usuario_id).eq('nombre', categoria_nombre).execute()
        
        if not response.data:
            return 0
        
        categoria_id = response.data[0]['id']
        
        # Obtener gastos
        response = supabase.table('movimientos').select('monto').eq('usuario_id', usuario_id).eq('categoria_id', categoria_id).eq('tipo', 'Gasto').gte('fecha', fecha_inicio).lte('fecha', fecha_fin).execute()
        
        return sum(mov['monto'] for mov in response.data) if response.data else 0
        
    except Exception as e:
        print(f"❌ Error al calcular gasto acumulado: {e}")
        return 0
