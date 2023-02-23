import { Component, OnInit } from '@angular/core';
import { Cancion } from './cancion';
import { CancionesService } from './canciones.service';

@Component({
  selector: 'app-canciones',
  templateUrl: './canciones.component.html',
  styleUrls: ['./canciones.component.css']
})
export class CancionesComponent implements OnInit {

  canciones: Array<Cancion>

  constructor(
    private cancionesSvc: CancionesService
  ) { }

  ngOnInit() {
    this.getListaCanciones()
  }

  getListaCanciones() {
    this.cancionesSvc.getAll('').subscribe(res => this.canciones = res)
  }
}
