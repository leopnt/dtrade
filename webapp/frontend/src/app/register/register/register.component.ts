import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  form = {
    username: null,
    email: null,
    password_hash: null
  }

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/api/v1/users', this.form).subscribe(
      data => console.log(data),
      err => console.log(err)
    )
  }


}
