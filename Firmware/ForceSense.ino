#include "HX711.h"

/*  
    Copyright 2018 Francesco Santini <francesco.santini@unibas.ch>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#define DATA_PIN 7
#define CLK_PIN 6
#define SCALE 2457.3f

HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("FS Force sensor");

  Serial.println("Initializing the scale");
  // parameter "gain" is omitted; the default value 128 is used by the library (channel A)
  scale.begin(DATA_PIN, CLK_PIN);

  scale.set_scale(SCALE);
  scale.tare(20);  // set the tare
}

void loop() {
  if (Serial.available() > 0)
  {
    // look for a command
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.equalsIgnoreCase("RESET"))
    {
      Serial.println("Resetting the tare");
      scale.tare(20);
      Serial.println("Done");
    }
  }
  // only execute if scale is ready to read a value
  if (scale.is_ready())
  {
    Serial.print("Force: ");
    float val = scale.get_units(); 
    Serial.println(val, 1);
  }
}
