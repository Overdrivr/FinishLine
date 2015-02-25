unsigned long starttime = 0, endtime = 0, duree = 0;

int afficheurs[] = {9,10,11,12,13};
int segments[8] = {8,A1,5,4,2,7,A2,6};
//6 Point
//8 a
// A1 b
//5 : c
//4 : d
//2 et 7 : f et e
//A2 : g


unsigned long i,j,k,l;
long sensorValue;

int decodeur[10][7] = {
{1,1,1,1,1,1,0},
{0,1,1,0,0,0,0},
{1,1,0,1,1,0,1},
{1,1,1,1,0,0,1},
{0,1,1,0,0,1,1},
{1,0,1,1,0,1,1},
{1,0,1,1,1,1,1},
{1,1,1,0,0,0,0},
{1,1,1,1,1,1,1},
{1,1,1,1,0,1,1}
};

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  pinMode(afficheurs[0], OUTPUT);
  pinMode(afficheurs[1], OUTPUT);
  pinMode(afficheurs[2], OUTPUT);
  pinMode(afficheurs[3], OUTPUT);
  pinMode(afficheurs[4], OUTPUT);
  pinMode(segments[0], OUTPUT);
  pinMode(segments[1], OUTPUT);  
  pinMode(segments[2], OUTPUT);  
  pinMode(segments[3], OUTPUT);  
  pinMode(segments[4], OUTPUT);
  pinMode(segments[5], OUTPUT);  
  pinMode(segments[6], OUTPUT);  
  pinMode(segments[7], OUTPUT);  
  Serial.begin(9600);
  i = 0, j = 0, k = 0,l = 0;
}

void loop() {  
  sensorValue = analogRead(A0);
  
  endtime = millis();
  duree = endtime - starttime;
  
  affiche_ms(duree);
  
  if(sensorValue < 70)
  {
    
    Serial.println(duree);
    i = 0;
    while(i < 25)
    {
      i++;
      affiche_ms(duree);
    }
    
    reset();
    delay(300);
    
    i=0;
    while(i < 25)
    {
      i++;
      affiche_ms(duree);
    }
       
    starttime = endtime;
  }
  delay(1);        // delay in between reads for stability
}



void affiche_ms(unsigned long ms)
{
   if(ms > 99999)
     ms /= 10;
     
   unsigned long digits[5];
   digits[0] = ms/10000;
   digits[1] = ms%10000/1000;
   digits[2] = ms%1000/100;
   digits[3] = ms%100/10;
   digits[4] = ms%10;
   
   affiche_nb(0,digits[0]);
   delay(5);
   affiche_nb(1,digits[1]);
   delay(5);
   affiche_nb(2,digits[2]);
   delay(5);
   affiche_nb(3,digits[3]);
   delay(5);
   affiche_nb(4,digits[4]);
   delay(5);
}

void affiche_nb(int afficheur, unsigned long valeur)
{
  reset();
  if(afficheur == 4)  
     digitalWrite(afficheurs[afficheur], HIGH);
  else
     digitalWrite(afficheurs[afficheur], LOW);
  
  for(k = 0 ; k < 7 ; k++)
  {
    if(afficheur == 4)
      digitalWrite(segments[k], -decodeur[valeur][k]+1);
    else
      digitalWrite(segments[k], decodeur[valeur][k]);
  }
  
  if(afficheur == 4)
    digitalWrite(segments[7], HIGH);
  else
    digitalWrite(segments[7], LOW);
  
}

void reset()
{
   digitalWrite(afficheurs[0], HIGH);
   digitalWrite(afficheurs[1], HIGH);
   digitalWrite(afficheurs[2], HIGH);
   digitalWrite(afficheurs[3], HIGH); 
   digitalWrite(afficheurs[4], LOW);
}

void testall()
{
  for(k = 0 ; k < 4 ; k++)
    digitalWrite(afficheurs[k], HIGH);
  digitalWrite(afficheurs[4], LOW);
  
  if(l == 4)  
     digitalWrite(afficheurs[l], HIGH);
   else
     digitalWrite(afficheurs[l], LOW);

  
  for(k = 0 ; k < 8 ; k++)
  {
    if(k == i)
    {
      if(l == 4)
       digitalWrite(segments[k], LOW);
      else
       digitalWrite(segments[k], HIGH);
    } 
    else
    {
      if(l == 4)
       digitalWrite(segments[k], HIGH);
      else
       digitalWrite(segments[k], LOW);
    } 
}
  Serial.print(i);
  delay(10);  
  j++;
  if(j>5)
  {
    i++;
    j=0;
  }
    
  if(i > 7)
  {
    i = 0;
    l++;
  }
  
  if(l > 4)
    l = 0;
}
