import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PedidoCompleto } from './interface/pedido';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PizzeriaService {

  constructor(private http: HttpClient) {}

  // GET: Consultar pedidos
  public getPedidos(): Observable<any> {
    return this.http.get<any>(
      'http://127.0.0.1:5000/api/pedidos/'
    );
  }

  // GET: Consultar un pedido
  public getPedido(id: number): Observable<any> {
    return this.http.get<any>(
      'http://127.0.0.1:5000/api/pedidos/' + id
    );
  }

  // POST: Registrar pedido
  public agregarPedido(datos: PedidoCompleto): Observable<any> {
    return this.http.post<any>(
      'http://127.0.0.1:5000/api/pedidos/',
      datos
    );
  }

  // GET: Consultar ventas por día
  public getVentasDia(dia: string): Observable<any> {
    return this.http.get<any>(
      'http://127.0.0.1:5000/api/ventas/dia?dia=' + dia
    );
  }

  // GET: Consultar ventas por mes
  public getVentasMes(mes: string): Observable<any> {
    return this.http.get<any>(
      'http://127.0.0.1:5000/api/ventas/mes?mes=' + mes
    );
  }

  // GET: Consultar detalle de venta
  public getDetalleVenta(id: number): Observable<any> {
    return this.http.get<any>(
      'http://127.0.0.1:5000/api/ventas/detalle/' + id
    );
  }

}