#!/usr/bin/perl -w

use strict;
use Net::FTP;

my $username = "anonymous";
my $pwd = "\n";
my $ftp = Net::FTP->new("ftp.ncbi.nlm.nih.gov") or die("connection not stablished with NCBI server: $!");  #Enter to NCBI databases
$ftp->login($username,$pwd) or die("incorrect login: $!");					# login and password for entering to databases

my $pathTObact = "/genomes/refseq/bacteria/";   							# path to bacterial genomes
$ftp->cwd("$pathTObact");  													# going to the path

my $Bacteria = '';
my @Directorios = $ftp->ls;

foreach $Bacteria (@Directorios) {				# Opening each subdirectory. This would loop through all available taxa of bacteria. $bacteria takes the taxon name.
	if ($Bacteria =~ /_/) {				
		$ftp->cwd("$Bacteria/");				# Entering the database for that particular taxon			
		my @archivos = $ftp->ls;				# listing all files inside

		foreach my $subdirectory (@archivos){		# Saco el archivo que está en el subdirectorio

			if ($subdirectory =~ /latest_assembly_versions/) {  # focusing only in last assemblies
#				print "$subdirectory\n";
				my $path = $pathTObact . $Bacteria. "/" . $subdirectory . "/";  # IMPORTANT --- NCBI uses references instead of physical folders some times.
																				# Here we set this path to return every time that we are sent to some other weird
																				# place.
				print $path;
				$ftp->cwd("$path");
				my @subdFiles = $ftp->ls;       # listing files inside the last assembly folder
				
				print "$subdFiles[0]\n";        # Inside we will find some REFERENCES of folders instead of actual folder. They look like GCF_001612905.1
												# We go to the first one and we will extract files only from this reference. Once we finish, we have to return tp 
												# the parental folder. But, given that this is a reference and not an actual folder, we will be in some other weir place. 
												# So, "cd .." or "cdup" would not work. Instad we need to use the path that we set before in $path. 
 				
				if ($subdFiles[0] =~ /^GCF/){
					$ftp->cwd("$subdFiles[0]");
					my @bacteriaFiles = $ftp->ls;
					
					foreach my $bacteriaFile (@bacteriaFiles){
						if ($bacteriaFile =~ /cds_from_genomic.fna.gz/){

#							print $ftp->pwd;
							print "$bacteriaFile\n";
							$ftp->binary;   # IMPORTANT --- Before transferring files, their server changes from binary to ASCII. It's important to change to "binary" again
											# otherwise the files that we transfer will be corrupted. 
											 
							$ftp->get("$bacteriaFile", "$bacteriaFile");  # getting file. 
							system("gunzip $bacteriaFile"); 		
						}
					}

					$ftp->cwd("$path");	# Return to "parental" path using "cd" or "cwd" and the path set above instead of "cd ..", explanation above.

				} else {
					print $ftp->pwd;
					print "\n";	
				}
				
				$ftp->cdup(); # Once it finishes with a lineage, we can go to next lineage by returning to parental folder. 
			}
		}		
		$ftp->cdup(); 	
	}
}

$ftp->quit or die("No se pudo desconectar con el servidor: $!");

# Este código me permite introducirme en las bases de datos del NCBI para descargar los genomas bacterianos para luego renombrarlos y guardarlos en un directorio local.

