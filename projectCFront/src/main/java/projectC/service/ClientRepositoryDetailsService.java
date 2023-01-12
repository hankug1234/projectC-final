package projectC.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import DTO.Client;
import projectC.repository.ClientRepositoryImp;

@Service
public class ClientRepositoryDetailsService implements UserDetailsService{
	private ClientRepositoryImp repository;
	@Autowired
	public  ClientRepositoryDetailsService(ClientRepositoryImp repository) {
		this.repository = repository;
	}
	
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException{
		Client client = repository.findByClientId(username);
		if(client != null) {
			return client;
		}
		throw new UsernameNotFoundException("clientid not found");
		
	}

}
