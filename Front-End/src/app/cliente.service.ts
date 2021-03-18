import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ClienteService {

  constructor(private httpClient: HttpClient) { }

  public getClientes(){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns1/cliente/`);
  }
  public getCliente(idcliente:any){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns1/cliente/${idcliente}`);
  }
  public deleteCliente(idcliente:any){
    return this.httpClient.delete(`http://127.0.0.1:5000/api/ns1/cliente/${idcliente}`);
  }
  public putClienteCadastrado(idcliente:any, cliente:any){
    return this.httpClient.put(`http://127.0.0.1:5000/api/ns1/cliente/${idcliente}`, cliente);
  }
  public postCliente(cliente:any){
    return this.httpClient.post(`http://127.0.0.1:5000/api/ns1/cliente/`, cliente);
  }


}
