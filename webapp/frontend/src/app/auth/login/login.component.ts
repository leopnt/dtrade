import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  form = {
    email: null,
    password: null
  }

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/auth/login', this.form).subscribe(
      data => console.log(data),
      err => console.log(err)
    )
  }

}
