import { Component } from '@angular/core';

import { Cliente } from '../cliente/cliente';
import { DetallePedido } from '../detalle-pedido/detalle-pedido';

import { Venta } from '../../interface/pedido';

@Component({
  selector: 'app-pedido',
  standalone: true,
  imports: [Cliente, DetallePedido],
  templateUrl: './pedido.html'
})
export class Pedido {

  datosCliente: any = null;

  pizzas: Venta[] = [];

  agregarPizza(datos: any): void {

    this.datosCliente = {
      nombre_cliente: datos.nombre_cliente,
      direccion: datos.direccion,
      telefono: datos.telefono,
      fecha_pedido: datos.fecha_pedido
    };

    this.pizzas = [...this.pizzas, datos.pizza];

  }

  quitarPizza(indice: number): void {

    this.pizzas = this.pizzas.filter(
      (_, i) => i !== indice
    );

  }

}