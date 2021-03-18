import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {ImovelService} from "../imovel.service";

@Component({
  selector: 'app-imovel',
  templateUrl: './imovel.component.html',
  styleUrls: ['./imovel.component.scss']
})
export class ImovelComponent implements OnInit {


 imovel: any

  constructor(private activatedRoute: ActivatedRoute, private apiService: ImovelService) {
    this.activatedRoute.queryParams.subscribe(params => {
      this.carregaImovel(Number(params['id']));
    });
  }

  ngOnInit(): void {


  }


  carregaImovel(imovelid: number) {
    this.apiService.getImovel(imovelid).subscribe(data => {
        this.imovel = data;
      },
      error => {
        console.log("Error", error);
      });
  }

  atualizaImovel(numero: string, imovelid: number) {
    this.apiService.putImovelCadastrado(imovelid, {
      "numero": Number(numero),
    }).subscribe(data => {
      },
      error => {
        console.log("Error", error);
      });
  }
}
