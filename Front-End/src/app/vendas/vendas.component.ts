import { Component, OnInit } from '@angular/core';
import {VendaService} from "../venda.service";

@Component({
  selector: 'app-vendas',
  templateUrl: './vendas.component.html',
  styleUrls: ['./vendas.component.scss']
})
export class VendasComponent implements OnInit {

  vendas:any; //{[index:string]:any} = {}
  hasVenda: boolean = false;

  constructor(private apiService: VendaService) { }
  ngOnInit() {
    this.apiService.getVendas().subscribe((data)=>{
      this.vendas = data;
      console.log(this.vendas);
      if ( (this.vendas.length == 0)){
        this.hasVenda = false;
      } else {
        this.hasVenda = true;
      }

    });
  }

  excluiVenda(imovelid:any){
    this.apiService.deleteVenda(imovelid).subscribe(data => {
    },
    error  => {
    console.log("Error", error);
    });
  }
}
