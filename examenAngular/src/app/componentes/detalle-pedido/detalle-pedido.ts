
import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PizzeriaService } from '../../pizzeria.service';
import { Venta } from '../../interface/pedido';

@Component({
  imports: [CommonModule],
  selector: 'app-detalle-pedido',
  templateUrl: './detalle-pedido.html',
})
export class DetallePedido {

  ngOnChanges(changes: SimpleChanges): void {
  this.calcularTotal();
 }
  @Input() pizzas: Venta[] = [];

  @Input() datosCliente: any;

  @Output() quitarPizza = new EventEmitter<number>();

  total: number = 0;

  constructor(public pizzeria: PizzeriaService) {}

  calcularTotal(): void {

    this.total = 0;

    for (let pizza of this.pizzas) {
      this.total += pizza.subtotal;
    }

  }

  eliminarPizza(indice: number): void {

    this.quitarPizza.emit(indice);

  }

  terminarPedido(): void {

    if (!this.datosCliente) {
      alert('Primero captura los datos del cliente');
      return;
    }

    if (this.pizzas.length === 0) {
      alert('Agrega al menos una pizza');
      return;
    }

    const pedido = {
      nombre_cliente: this.datosCliente.nombre_cliente,
      direccion: this.datosCliente.direccion,
      telefono: this.datosCliente.telefono,
      fecha_pedido: this.datosCliente.fecha_pedido,
      pizzas: this.pizzas
    };

    this.pizzeria.agregarPedido(pedido).subscribe({

      next: (response) => {

        if (response.exito) {

          alert('Pedido registrado correctamente. Total a pagar: $' + response.total);

          this.pizzas = [];
          this.total = 0;

        } else {

          alert('No se pudo registrar el pedido');

        }

      },

      error: (error) => {

        console.error('Error al registrar el pedido:', error);

        alert('Ocurrió un error al registrar el pedido');

      }

    });

  }

}
