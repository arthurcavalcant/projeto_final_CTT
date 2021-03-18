import { Component, OnInit } from '@angular/core';
import {ClienteService} from "../cliente.service";

@Component({
  selector: 'app-novo-cliente',
  templateUrl: './novo-cliente.component.html',
  styleUrls: ['./novo-cliente.component.scss']
})
export class NovoClienteComponent implements OnInit {

  constructor(private apiService: ClienteService) { }

  ngOnInit(): void {
  }

  insereNovoCliente(nome: string, cpf: string, rg: string, data_nascimento: string, estado_civil: string, profissao: string) {

    this.apiService.postCliente({ "nome":nome, "cpf": cpf, "rg":rg, "data_nascimento":data_nascimento,
      "estado_civil_pessoa": estado_civil, "profissao":profissao}).subscribe(data => {
      },
      error  => {
      console.log("Error", error);
      });
  }
}
