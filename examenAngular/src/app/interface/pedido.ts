export interface Pedido {
  id_pedido?: number;
  nombre_cliente: string;
  direccion: string;
  telefono: string;
  fecha_pedido: string;
  total?: number;
}

export interface Venta {
  id_venta?: number;
  id_pedido?: number;
  tamano: string;
  ingredientes: string[];
  cantidad: number;
  subtotal: number;
}

export interface PedidoCompleto {
  nombre_cliente: string;
  direccion: string;
  telefono: string;
  fecha_pedido: string;
  pizzas: Venta[];
}