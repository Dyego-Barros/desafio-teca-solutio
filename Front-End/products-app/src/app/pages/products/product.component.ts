import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Product } from '../../core/models/product.model';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product.component.html'
})
export class ProductComponent {

  products: Product[] = [];
  model: Product = this.resetModel();
  message = '';

  private baseUrl = 'http://127.0.0.1:5000/product';

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.load();
  }

  // Pega token do localStorage
  private getAuthHeaders(): HttpHeaders | null {
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigate(['/login']);
      return null;
    }
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  // GET /list
  load() {
    const headers = this.getAuthHeaders();
    if (!headers) return;

    this.http.get<Product[]>(`${this.baseUrl}/list`, { headers }).subscribe({
      next: (data: Product[]) => {
        console.log('Produtos recebidos da API:', data);
        this.products = data;
        this.cdr.detectChanges(); // força atualização imediata
      },
      error: (e) => console.error('Erro ao carregar produtos:', e)
    });
  }

  // POST /create ou PUT /update/:id
  save() {
    const headers = this.getAuthHeaders();
    if (!headers) return;

    if (this.model.id) {
      // Atualização
      this.http.put(`${this.baseUrl}/update/${this.model.id}`, this.model, { headers }).subscribe({
        next: () => {
          this.message = 'Produto atualizado!';
          this.resetForm();
          this.load();
        },
        error: (e) => console.error('Erro ao atualizar produto:', e)
      });
    } else {
      // Criação
      this.http.post(`${this.baseUrl}/create`, this.model, { headers }).subscribe({
        next: () => {
          this.message = 'Produto salvo!';
          this.resetForm();
          this.load();
        },
        error: (e) => console.error('Erro ao criar produto:', e)
      });
    }
  }

  // Editar produto localmente
  edit(p: Product) {
    this.model = { ...p };
  }

  // DELETE /delete/:id
  delete(p: Product) {
    if (!p.id) return;

    const headers = this.getAuthHeaders();
    if (!headers) return;

    this.http.delete(`${this.baseUrl}/delete/${p.id}`, { headers }).subscribe({
      next: () => {
        this.message = 'Produto excluído!';
        this.load();
        if (this.model.id === p.id) this.resetForm();
      },
      error: (e) => console.error('Erro ao excluir produto:', e)
    });
  }

  resetForm() {
    this.model = this.resetModel();
  }

  private resetModel(): Product {
    return { nome: '', marca: '', valor: 0, in_stock: true };
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}
