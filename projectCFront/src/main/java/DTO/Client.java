package DTO;

import java.io.Serializable;
import java.util.Arrays;
import java.util.Collection;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

public class Client implements Serializable , UserDetails{
	private static final long serialVersionUID = 1L;
	private String username;
	private String password;
	private String repw;
	
	public Client() {
		
	}
	
	public Client(String id,String pw) {
		this.username= id;
		this.password = pw;
	}
	
	public String getUsername() {
		return this.username;
	}
	public String getPassword() {
		return this.password;
	}
	public String getRepw() {
		return this.repw;
	}
	
	public void setUsername(String id) {
		this.username = id;
	}
	
	public void setPassword(String pw) {
		this.password = pw;
	}
	
	public void setRepw(String repw) {
		this.repw = repw;
	}
	
	
	public Collection<? extends GrantedAuthority> getAuthorities(){
		return Arrays.asList(new SimpleGrantedAuthority("login"));
	}
	
	public boolean isAccountNonExpired() {
		return true;
	}
	
	public boolean isAccountNonLocked() {
		return true;
	}
	
	public boolean isCredentialsNonExpired() {
		return true;
	}
	
	public boolean isEnabled() {
		return true;
	}
}
