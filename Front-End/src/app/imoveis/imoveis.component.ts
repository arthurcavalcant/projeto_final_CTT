import { Component, OnInit } from '@angular/core';
import {ImovelService} from "../imovel.service";

@Component({
  selector: 'app-imoveis',
  templateUrl: './imoveis.component.html',
  styleUrls: ['./imoveis.component.scss']
})
export class ImoveisComponent implements OnInit {

imoveis:any; //{[index:string]:any} = {}
  hasImovel: boolean = false;
  constructor(private apiService: ImovelService) { }
  ngOnInit() {
    this.apiService.getImoveis().subscribe((data)=>{
      this.imoveis = data;
      console.log(this.imoveis);
      if ( (this.imoveis.length == 0)){
        this.hasImovel = false;
      } else {
        this.hasImovel = true;
      }

    });
  }

  excluiImovel(imovelid:any){
    this.apiService.deleteImovel(imovelid).subscribe(data => {
    },
    error  => {
    console.log("Error", error);
    });
  }
}
