import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { ProductComponent } from './pages/products/product.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
   { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: ProductComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
