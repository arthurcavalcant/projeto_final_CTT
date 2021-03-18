import { Component, OnInit } from '@angular/core';
import {ProprietarioService} from "../proprietario.service";

@Component({
  selector: 'app-proprietarios',
  templateUrl: './proprietarios.component.html',
  styleUrls: ['./proprietarios.component.scss']
})
export class ProprietariosComponent implements OnInit {
proprietarios:any; //{[index:string]:any} = {}
  hasProprietario: boolean = false;
  constructor(private apiService: ProprietarioService) { }
  ngOnInit() {
    this.apiService.getProprietarios().subscribe((data)=>{
      this.proprietarios = data;
      if ( (this.proprietarios.length == 0)){
        this.hasProprietario = false;
      } else {
        this.hasProprietario = true;
      }

    });
  }

  excluiProprietario(proprietarioid:any){
    this.apiService.deleteProprietario(proprietarioid).subscribe(data => {
    },
    error  => {
    console.log("Error", error);
    });
  }
}

