import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface LoginResponse {
  token: string; // ajuste conforme sua API
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private tokenKey = 'token';
  private baseUrl = 'http://127.0.0.1:5000/user'; // ajuste para sua API

  constructor(private http: HttpClient) {}

  // Faz login e retorna Observable
  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, { email, password });
  }

  // Salva token no localStorage
  setToken(token: string) {
    localStorage.setItem(this.tokenKey, token);
    console.log('token do storage', token)
  }

  // Retorna token armazenado
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  // Remove token (logout)
  logout() {
    localStorage.removeItem(this.tokenKey);
  }

  // Retorna true se estiver logado
  isLogged(): boolean {
    return !!this.getToken();
  }
}
