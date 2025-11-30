import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Product } from '../models/product.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private baseUrl = 'http://127.0.0.1:5000/product';

  constructor(private http: HttpClient) {}

  // GET /product/list → lista todos os produtos
  getAll(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.baseUrl}/list`);
  }

  // POST /product/create → cria produto
  create(product: Product): Observable<any> {
    return this.http.post(`${this.baseUrl}/create`, product);
  }

  // PUT /product/update/:id → atualiza produto
  update(id: number | string, product: Product): Observable<any> {
    return this.http.put(`${this.baseUrl}/update/${id}`, product);
  }

  // DELETE /product/delete/:id → remove produto
  delete(id: number | string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete/${id}`);
  }
}
