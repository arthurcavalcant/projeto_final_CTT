import { Component, OnInit } from '@angular/core';
import {VendedorService} from "../vendedor.service";

@Component({
  selector: 'app-novo-vendedor',
  templateUrl: './novo-vendedor.component.html',
  styleUrls: ['./novo-vendedor.component.scss']
})
export class NovoVendedorComponent implements OnInit {

  constructor(private apiService: VendedorService) { }

  ngOnInit(): void {
  }

  insereNovoVendedor(nome: string, cpf: string, rg: string, data_nascimento: string, estado_civil: string, profissao: string) {

    this.apiService.postVendedor({ "nome":nome, "cpf": cpf, "rg":rg, "data_nascimento":data_nascimento,
      "estado_civil_pessoa": estado_civil, "profissao":profissao}).subscribe(data => {
      },
      error  => {
      console.log("Error", error);
      });
  }
}
