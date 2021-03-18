import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {VendedorService} from "../vendedor.service";

@Component({
  selector: 'app-vendedor',
  templateUrl: './vendedor.component.html',
  styleUrls: ['./vendedor.component.scss']
})
export class VendedorComponent implements OnInit {
vendedor: any

  constructor(private activatedRoute: ActivatedRoute, private apiService: VendedorService) {
    this.activatedRoute.queryParams.subscribe(params => {
      this.carregaVendedor(Number(params['id']));
    });
  }

  ngOnInit(): void {


  }


  carregaVendedor(vendedorid: number) {
    this.apiService.getVendedor(vendedorid).subscribe(data => {
        this.vendedor = data;
      },
      error => {
        console.log("Error", error);
      });
  }

  atualizaVendedor(nome: string, estado_civil: string, profissao: string, vendedorid: number) {
    this.apiService.putVendedorCadastrado(vendedorid, {
      "nome": nome,
      "estado_civil_pessoa": estado_civil,
      "profissao": profissao
    }).subscribe(data => {
      },
      error => {
        console.log("Error", error);
      });
  }
}

