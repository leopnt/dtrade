import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';


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

  server_error = false;

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
  }
  onSubmit() {
    this.http.post('http://127.0.0.1:5000/api/v1/users', this.form).subscribe(
      (response) => {
        this.authService.isLogged = true
        this.router.navigate(['sub'])
      },
      (err: HttpErrorResponse) => {
        console.log(err);
      }
    )
  }
}
