import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
    standalone: true,
    imports: [FormsModule, CommonModule],
    template: `
    <h2 style="text-align:center;">Panel Admin 💎</h2>

    <div style="text-align:center;">
    <input [(ngModel)]="producto.nombre" placeholder="Nombre">
    <input [(ngModel)]="producto.tipo" placeholder="Tipo">
    <input [(ngModel)]="producto.precio" placeholder="Precio">
    <input [(ngModel)]="producto.peso" placeholder="Peso">
    <input [(ngModel)]="producto.diametro" placeholder="Diámetro">
    <input [(ngModel)]="producto.material" placeholder="Material">

    <button (click)="crear()">Crear Producto</button>
    </div>

    <hr>

    <div style="display:flex; flex-wrap:wrap; justify-content:center;">
    <div class="card" *ngFor="let p of productos">
        <h3>{{p.nombre}}</h3>
        <p>💰 {{p.precio}}</p>
        <p>⚖️ {{p.peso}}</p>
        <button (click)="eliminar(p._id)">Eliminar</button>
    </div>
    </div>
    `
})
export class AdminComponent implements OnInit {

    producto: any = { nombre: '', tipo: '', precio: '', peso: '', diametro: '', material: '' };
    productos: any[] = [];

    ngOnInit(){
    this.cargar();
    }

  // 🔍 cargar productos
    cargar(){
    fetch('http://localhost:3000/api/productos')
        .then(res => res.json())
        .then(data => {
        this.productos = data || [];
        });
    }

  // 💾 crear producto
    crear(){
    if (!this.producto) return;
    fetch('http://localhost:3000/api/productos', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.producto)
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        alert('Producto creado 💎');
        this.producto = {};
        this.cargar();
    })
    .catch(err => console.error(err));
    }

  // ❌ eliminar
    eliminar(id:string){
    fetch(`http://localhost:3000/api/productos/${id}`, {
        method: 'DELETE'
    })
    .then(() => {
        alert('Producto eliminado ❌');
        this.cargar();
    });
    }
}