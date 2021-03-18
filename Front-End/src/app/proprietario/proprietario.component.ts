import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {ProprietarioService} from "../proprietario.service";

@Component({
  selector: 'app-proprietario',
  templateUrl: './proprietario.component.html',
  styleUrls: ['./proprietario.component.scss']
})
export class ProprietarioComponent implements OnInit {

 proprietario: any

  constructor(private activatedRoute: ActivatedRoute, private apiService: ProprietarioService) {
    this.activatedRoute.queryParams.subscribe(params => {
      this.carregaProprietario(Number(params['id']));
    });
  }

  ngOnInit(): void {


  }


  carregaProprietario(proprietarioid: number) {
    this.apiService.getProprietario(proprietarioid).subscribe(data => {
        this.proprietario = data;
      },
      error => {
        console.log("Error", error);
      });
  }

  atualizaProprietario(nome: string, estado_civil: string, profissao: string, proprietarioid: number) {
    this.apiService.putProprietarioCadastrado(proprietarioid, {
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

