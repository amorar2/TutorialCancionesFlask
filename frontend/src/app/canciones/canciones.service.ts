import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { Cancion } from './cancion';

@Injectable({
  providedIn: 'root'
})
export class CancionesService {

constructor(private http: HttpClient) { }
  URL = "http://localhost:5000"

  public getAll(nombre: string): Observable<Cancion[]> {
    return this.http.get<Cancion[]>(`${this.URL}/canciones`)
  }
}
