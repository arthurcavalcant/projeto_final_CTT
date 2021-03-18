import {Component, OnInit} from '@angular/core';
import {ClienteService} from "../cliente.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-cliente',
  templateUrl: './cliente.component.html',
  styleUrls: ['./cliente.component.scss']
})
export class ClienteComponent implements OnInit {

  cliente: any

  constructor(private activatedRoute: ActivatedRoute, private apiService: ClienteService) {
    this.activatedRoute.queryParams.subscribe(params => {
      this.carregaCliente(Number(params['id']));
    });
  }

  ngOnInit(): void {


  }


  carregaCliente(clienteid: number) {
    this.apiService.getCliente(clienteid).subscribe(data => {
        this.cliente = data;
      },
      error => {
        console.log("Error", error);
      });
  }

  atualizaCliente(nome: string, estado_civil: string, profissao: string, clienteid: number) {
    this.apiService.putClienteCadastrado(clienteid, {
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
