import { Component, OnInit } from '@angular/core';
import { ClienteService } from '../cliente.service';

@Component({
  selector: 'app-clientes',
  templateUrl: './clientes.component.html',
  styleUrls: ['./clientes.component.scss']
})
export class ClientesComponent implements OnInit {
  clientes:any; //{[index:string]:any} = {}
  hasCliente: boolean = false;
  constructor(private apiService: ClienteService) { }
  ngOnInit() {
    this.apiService.getClientes().subscribe((data)=>{
      console.log(data);
      this.clientes = data;
      if ( (this.clientes.length == 0)){
        this.hasCliente = false;
      } else {
        this.hasCliente = true;
      }

    });
  }

  excluiCliente(clienteid:any){
    this.apiService.deleteCliente(clienteid).subscribe(data => {
      console.log(clienteid);
    },
    error  => {
    console.log("Error", error);
    });
  }
}
