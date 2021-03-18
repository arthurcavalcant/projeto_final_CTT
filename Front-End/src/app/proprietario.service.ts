import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ProprietarioService {
  constructor(private httpClient: HttpClient) { }

  public getProprietarios(){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns2/proprietario/`);
  }
  public getProprietario(idproprietario:any){
    return this.httpClient.get(`http://127.0.0.1:5000/api/ns2/proprietario/${idproprietario}`);
  }
  public deleteProprietario(idproprietario:any){
    return this.httpClient.delete(`http://127.0.0.1:5000/api/ns2/proprietario/${idproprietario}`);
  }
  public putProprietarioCadastrado(idproprietario:any, proprietario:any){
    return this.httpClient.put(`http://127.0.0.1:5000/api/ns2/proprietario/${idproprietario}`, proprietario);
  }
  public postProprietario(proprietario:any){
    return this.httpClient.post(`http://127.0.0.1:5000/api/ns2/proprietario/`, proprietario);
  }


}
