import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {

  username = '';  // será usado como email
  password = '';
  loading = false;
  errorMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  submit() {
    this.errorMessage = '';
    this.loading = true;

    if (!this.username || !this.password) {
      this.errorMessage = 'Preencha email e senha.';
      this.loading = false;
      return;
    }

    this.authService.login(this.username, this.password).subscribe({
      next: (res) => {
        console.log('Login OK', res);
        console.log('Resposta completa:', res.token);
        // 🔥 Salvar token (ajuste o campo conforme sua API)
        this.authService.setToken(res.token);

        console.log('Token:', this.authService.getToken());
        // 🔥 Redirecionar
        this.router.navigate(['/dashboard']);

        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Email ou senha inválidos.';
        this.loading = false;
      }
    });
  }
}
