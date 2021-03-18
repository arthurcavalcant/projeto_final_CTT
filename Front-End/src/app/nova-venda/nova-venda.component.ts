import { Component, OnInit } from '@angular/core';
import {VendaService} from "../venda.service";

@Component({
  selector: 'app-nova-venda',
  templateUrl: './nova-venda.component.html',
  styleUrls: ['./nova-venda.component.scss']
})
export class NovaVendaComponent implements OnInit {

  constructor(private apiService: VendaService) { }

  ngOnInit(): void {
  }

  insereNovaVenda(id_imovel: string, id_proprietario: string, id_cliente: string, id_vendedor: string, tipo_venda: string, valor: string) {

    this.apiService.postVenda({ "id_imovel":id_imovel, "id_cliente": id_cliente, "id_proprietario":id_proprietario,
      "id_vendedor":id_vendedor, "valor": Number(valor), "tipo_venda":tipo_venda}).subscribe(data => {
      },
      error  => {
      console.log("Error", error);
      });
  }
}
