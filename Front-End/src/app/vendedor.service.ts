import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class VendedorService {

    constructor(private httpClient: HttpClient) { }

  public getVendedores(){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns3/vendedor/`);
  }
  public getVendedor(idvendedor:any){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns3/vendedor/${idvendedor}`);
  }
  public deleteVendedor(idvendedor:any){
    return this.httpClient.delete(`http://127.0.0.1:5000/api/ns3/vendedor/${idvendedor}`);
  }
  public putVendedorCadastrado(idvendedor:any, vendedor:any){
    return this.httpClient.put(`http://127.0.0.1:5000/api/ns3/vendedor/${idvendedor}`, vendedor);
  }
  public postVendedor(vendedor:any){
    return this.httpClient.post(`http://127.0.0.1:5000/api/ns3/vendedor/`, vendedor);
  }


}
