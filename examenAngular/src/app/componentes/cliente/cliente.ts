
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  imports: [CommonModule, ReactiveFormsModule],
  selector: 'app-cliente',
  templateUrl: './cliente.html',
})
export class Cliente implements OnInit {

  @Output() agregarPizza = new EventEmitter<any>();

  formulario!: FormGroup;

  precioTamano: number = 0;
  precioIngredientes: number = 0;

  constructor(public fb: FormBuilder) {}

  ngOnInit(): void {

    this.formulario = this.fb.group({
      nombre_cliente: ['', Validators.required],
      direccion: ['', Validators.required],
      telefono: ['', Validators.required],
      fecha_pedido: ['', Validators.required],

      tamano: ['Chica', Validators.required],

      jamon: [false],
      pina: [false],
      champinones: [false],

      cantidad: [1, [Validators.required, Validators.min(1)]]
    });

  }

  agregar(): void {

    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }

    const datos = this.formulario.getRawValue();

    // Obtener precio del tamaño
    switch (datos.tamano) {
      case 'Chica':
        this.precioTamano = 40;
        break;

      case 'Mediana':
        this.precioTamano = 80;
        break;

      case 'Grande':
        this.precioTamano = 120;
        break;
    }

    // Obtener ingredientes seleccionados
    let ingredientes: string[] = [];

    this.precioIngredientes = 0;

    if (datos.jamon) {
      ingredientes.push('Jamón');
      this.precioIngredientes += 10;
    }

    if (datos.pina) {
      ingredientes.push('Piña');
      this.precioIngredientes += 10;
    }

    if (datos.champinones) {
      ingredientes.push('Champiñones');
      this.precioIngredientes += 10;
    }

    const subtotal =
      (this.precioTamano + this.precioIngredientes) * datos.cantidad;

    const pedido = {
      nombre_cliente: datos.nombre_cliente,
      direccion: datos.direccion,
      telefono: datos.telefono,
      fecha_pedido: datos.fecha_pedido,

      pizza: {
        tamano: datos.tamano,
        ingredientes: ingredientes,
        cantidad: datos.cantidad,
        subtotal: subtotal
      }
    };

    this.agregarPizza.emit(pedido);

    alert('Pizza agregada correctamente');

    // Reiniciar selección de pizza
    this.formulario.patchValue({
      tamano: 'Chica',
      jamon: false,
      pina: false,
      champinones: false,
      cantidad: 1
    });

  }

}
