
import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PizzeriaService } from '../../pizzeria.service';

@Component({
  selector: 'app-ventas',
  imports: [CommonModule, FormsModule],
  templateUrl: './ventas.html'
})
export class Ventas {

  dia: string = 'lunes';
  mes: string = 'enero';

  ventas: any[] = [];
  pedidoSeleccionado: any = null;

  constructor(
    public pizzeria: PizzeriaService,
    private cdr: ChangeDetectorRef
  ) {}

  consultarDia(): void {
    this.pedidoSeleccionado = null;

    this.pizzeria.getVentasDia(this.dia).subscribe({
      next: (response) => {
        this.ventas = response.ventas || [];
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error al consultar ventas por día:', error);
        alert('No se pudieron consultar las ventas');
      }
    });
  }

  consultarMes(): void {
    this.pedidoSeleccionado = null;

    this.pizzeria.getVentasMes(this.mes).subscribe({
      next: (response) => {
        this.ventas = response.ventas || [];
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error al consultar ventas por mes:', error);
        alert('No se pudieron consultar las ventas');
      }
    });
  }

  consultarDetalle(id: number): void {

    this.pedidoSeleccionado = null;

    this.pizzeria.getPedido(id).subscribe({
      next: (response) => {

        console.log('Respuesta del pedido:', response);

        const pedido = response.pedido || response;

        this.pedidoSeleccionado = {
          ...pedido,
          pizzas: pedido.pizzas || pedido.ventas ||
                  response.pizzas || response.ventas || []
        };

        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error al consultar el pedido:', error);
        alert('No se pudo consultar el detalle del pedido');
      }
    });
  }

}
