import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  standalone: true,
  imports: [FormsModule],
  template: `
  <h2>Registro</h2>

  <input [(ngModel)]="user.nombre" placeholder="Nombre">
  <input [(ngModel)]="user.email" placeholder="Email">
  <input [(ngModel)]="user.password" placeholder="Password">

  <button (click)="registrar()">Registrarse</button>
  `
})
export class RegistroComponent {

  user:any = {};

  constructor(private auth:AuthService){}

  registrar(){
    this.auth.registro(this.user).subscribe(()=>{
      alert('Registrado correctamente 💎');
    });
  }
}