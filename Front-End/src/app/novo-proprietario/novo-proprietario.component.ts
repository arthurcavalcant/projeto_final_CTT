import { Component, OnInit } from '@angular/core';
import {ProprietarioService} from "../proprietario.service";

@Component({
  selector: 'app-novo-proprietario',
  templateUrl: './novo-proprietario.component.html',
  styleUrls: ['./novo-proprietario.component.scss']
})
export class NovoProprietarioComponent implements OnInit {

  constructor(private apiService: ProprietarioService) { }

  ngOnInit(): void {
  }

  insereNovoProprietario(nome: string, cpf: string, rg: string, data_nascimento: string, estado_civil: string, profissao: string) {

    this.apiService.postProprietario({ "nome":nome, "cpf": cpf, "rg":rg, "data_nascimento":data_nascimento,
      "estado_civil_pessoa": estado_civil, "profissao":profissao}).subscribe(data => {
      },
      error  => {
      console.log("Error", error);
      });
  }
}
