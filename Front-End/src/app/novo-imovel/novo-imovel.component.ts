import { Component, OnInit } from '@angular/core';
import {ImovelService} from "../imovel.service";

@Component({
  selector: 'app-novo-imovel',
  templateUrl: './novo-imovel.component.html',
  styleUrls: ['./novo-imovel.component.scss']
})
export class NovoImovelComponent implements OnInit {

  constructor(private apiService: ImovelService) { }

  ngOnInit(): void {
  }

  insereNovoImovel(id_proprietario: string, tipo_imovel: string, rua: string, numero: string, andar: string, bloco: string,
                   cep: string, cidade: string, uf: string, data_posse_proprietario: string) {

    this.apiService.postImovel({ "id_proprietario":Number(id_proprietario),"tipo_imovel":tipo_imovel, "rua": rua, "numero":Number(numero), "andar":Number(andar),
      "bloco": bloco, "cep":cep, "cidade":cidade, "uf":uf, "data_posse_proprietario": data_posse_proprietario}).subscribe(data => {
      },
      error  => {
      console.log("Error", error);
      });
  }
}
