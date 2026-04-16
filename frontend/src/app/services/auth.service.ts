import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {

    API = 'http://localhost:3000/api/auth';

    constructor(private http: HttpClient) {}

    registro(data:any){
    return this.http.post(this.API + '/registro', data);
    }

    login(data:any){
    return this.http.post<any>(this.API + '/login', data);
    }
}