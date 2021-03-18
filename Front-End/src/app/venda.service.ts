import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class VendaService {

   constructor(private httpClient: HttpClient) { }

  public getVendas(){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns5/venda/`);
  }
  public deleteVenda(idvenda:any){
    return this.httpClient.delete(`http://127.0.0.1:5000/api/ns5/venda/${idvenda}`);
  }
  public postVenda(venda:any){
    return this.httpClient.post(`http://127.0.0.1:5000/api/ns5/venda/`, venda);
  }

}
