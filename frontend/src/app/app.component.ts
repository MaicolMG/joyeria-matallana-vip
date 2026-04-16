import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterOutlet, RouterLink],
    template: `
    <nav>
    <a routerLink="/login">Login</a> |
    <a routerLink="/registro">Registro</a> |
    <a routerLink="/productos">Productos</a> |
    <a routerLink="/admin">Admin</a>
    </nav>

    <router-outlet></router-outlet>
    `
})
export class AppComponent {}