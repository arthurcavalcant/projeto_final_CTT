import { Component, OnInit } from '@angular/core';
import {VendedorService} from "../vendedor.service";

@Component({
  selector: 'app-vendedores',
  templateUrl: './vendedores.component.html',
  styleUrls: ['./vendedores.component.scss']
})
export class VendedoresComponent implements OnInit {
  vendedores:any; //{[index:string]:any} = {}
  hasVendedor: boolean = false;
  constructor(private apiService: VendedorService) { }
  ngOnInit() {
    this.apiService.getVendedores().subscribe((data)=>{
      console.log(data);
      this.vendedores = data;
      if ( (this.vendedores.length == 0)){
        this.hasVendedor = false;
      } else {
        this.hasVendedor = true;
      }

    });
  }

  excluiVendedor(vendedorid:any){
    this.apiService.deleteVendedor(vendedorid).subscribe(data => {
      console.log(vendedorid);
    },
    error  => {
    console.log("Error", error);
    });
  }
}
