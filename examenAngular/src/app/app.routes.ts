import { Routes } from '@angular/router';

export const routes: Routes = [

  {
    path: 'pizzeria',
    children: [

      {
        path: 'pedido',
        loadComponent: () =>
          import('./componentes/pedido/pedido').then(
            (c) => c.Pedido
          )
      },

      {
        path: 'ventas',
        loadComponent: () =>
          import('./componentes/ventas/ventas').then(
            (c) => c.Ventas
          )
      }

    ]
  },

  {
    path: '',
    redirectTo: 'pizzeria/pedido',
    pathMatch: 'full'
  },

  {
    path: '**',
    redirectTo: 'pizzeria/pedido'
  }

];