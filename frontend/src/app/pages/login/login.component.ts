import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
    standalone: true,
    imports: [FormsModule],
    template: `
    <h2>Login</h2>

    <input [(ngModel)]="data.email" placeholder="Email">
    <input [(ngModel)]="data.password" placeholder="Password">

    <button (click)="login()">Ingresar</button>
    `
})
export class LoginComponent {

    data:any = {};

    constructor(private auth:AuthService){}

    login(){
    this.auth.login(this.data).subscribe((res:any)=>{
        localStorage.setItem('token', res.token);
        alert('Bienvenido 💎');
    });
    }
}