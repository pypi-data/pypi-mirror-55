def rsa():
    print('''
 import math
'''
#def Prime(num):
#    for i in range(2, num):
#        if(num % i  == 0):
#            return("no")
#    return("yes")
'''
p=int(input("Enter a prime number:"))
q=int(input("Enter a prime number:"))
n=p*q
j,k=2,1
tn=(p-1)*(q-1)
print("tn=",tn)
#for finding value of e
for i in range(tn):
    if(math.gcd(j,tn) == 1):
        #if(Prime(j)=="yes"):
        e=j
        break
    j+=1
print("e=",e)
#for finding value of d
while(True):
    if((e*k)%tn == 1):
        d=k
        break
    k+=1
print("d=",d)
text=input("enter the plain text:")
text1=""
text2=""
for t in text:
    print(ord(t))
    w=chr((ord(t)**e)%n)
    text1+=w
print(text1)
for t in text1:
    w=chr((ord(t)**d)%n)
    text2+=w
print(text2)
    ''')
def deffie():
    print('''

# input values ye hi dena 11,5,7,3

p=int(input("enter the prime number:"))
g=int(input("enter the numberless than p:"))
x=int(input("enter the alice key(prime number):"))
y=int(input("enter the bob key(prime number):"))
ra=g**x
rb=g**y
r1=ra%p
r2=rb%p
ka=r1**x
kb=r2**y
k1=ka%p
k2=kb%p
print("ra={},rb={},r1={},r2={},ka={},kb={},k1={},k2={}".format(ra,rb,r1,r2,ka,kb,k1,k2))
kn=g**(x*y)
k=kn%p
print(k)
text=input("Enter the plain text:")
text1=""
text2=""
for i in text:
    #print(ord(i)+key)
    t=chr(ord(i)+k)
    text1+=t
print("The encr text is:"+text1)
for i in text1:
    t=chr(ord(i)-k)
    text2+=t
print("The deencr text is:"+text2)
    ''')
def DemoMaps():
	print('''
	_______________activity_maps.XML______________
	<?xml version="1.0" encoding="utf-8"?>

<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"

    xmlns:android="http://schemas.android.com/apk/res/android">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:weightSum="2">
        <EditText
            android:id="@+id/edt_loc"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:hint="Enter Location."
            android:padding="20dp"
            android:inputType="text"
            android:layout_weight="1"
            />
        <Button
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:padding="20dp"
            android:text="Search"
            android:id="@+id/btn_search"
            android:onClick="searchLoc"
            android:layout_weight="1"
            />
    </LinearLayout>
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:weightSum="3">
        <Button
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:padding="20dp"
            android:text="Zoom In"
            android:id="@+id/btn_zoomIn"
            android:onClick="zoomControl"
            android:layout_weight="1"
            />
        <Button
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:padding="20dp"
            android:text="Zoom Out"
            android:id="@+id/btn_zoomOut"
            android:onClick="zoomControl"
            android:layout_weight="1"
            />
        <Button
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:padding="20dp"
            android:text="Change type"
            android:id="@+id/btn_change"
            android:onClick="changeMap"
            android:layout_weight="1"
            />
    </LinearLayout>


    <fragment xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:map="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/map"
    android:name="com.google.android.gms.maps.SupportMapFragment"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MapsActivity" />

</LinearLayout>

___________________MapsActivity.JAVA_______________
______________________________________
package com.example.demomaps;

import androidx.fragment.app.FragmentActivity;

import android.location.Address;
import android.location.Geocoder;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.IOException;
import java.util.List;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
//        LatLng sydney = new LatLng(-34, 151);
//        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
//        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));

        mMap.setMyLocationEnabled(true);
    }
    public void searchLoc(View v)
    {
        EditText mLoc = findViewById(R.id.edt_loc);
        String str_loc = mLoc.getText().toString();
        List<Address> mAdd = null;
        if(str_loc!=null)
        {
            Geocoder geocoder = new Geocoder(this);
            try {
                mAdd = geocoder.getFromLocationName(str_loc,1);
            } catch (IOException e) {
                e.printStackTrace();
            }

            Address address = mAdd.get(0);

            LatLng latLng = new LatLng(address.getLatitude(),address.getLongitude());

            mMap.addMarker(new MarkerOptions().position(latLng).title(str_loc));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(latLng));

        }

    }

    public void zoomControl(View v)
    {
        if(v.getId() == R.id.btn_zoomIn)
        {
            mMap.moveCamera(CameraUpdateFactory.zoomIn());

        }

        else
        {
            mMap.moveCamera(CameraUpdateFactory.zoomOut());
        }
    }

    public void changeMap(View v)
    {
        if(mMap.getMapType() == GoogleMap.MAP_TYPE_NORMAL)
        {
            mMap.setMapType(GoogleMap.MAP_TYPE_SATELLITE);
        }
        else
        {
            mMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        }
    }
}

	''')
def SQLiteApp():
	print('''
	_________________________activity_main.xml____________
	________________________________________
	<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity"
    android:orientation="vertical">

    <EditText
        android:id="@+id/id_edt"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter ID Here..."
        android:inputType="number"
        android:padding="20dp"
        android:layout_margin="20dp"
        >

    </EditText>
    <EditText
        android:id="@+id/name_edt"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter Name Here..."
        android:inputType="text"
        android:padding="20dp"
        android:layout_margin="20dp"
        >

    </EditText>
    <EditText
        android:id="@+id/mobile_edt"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter Mobile Here...."
        android:inputType="number"
        android:padding="20dp"
        android:layout_margin="20dp"
        >

    </EditText>
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:weightSum="2"

        >
        <Button
            android:id="@+id/btn_add"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="ADD"
            android:layout_weight="1"
            android:onClick="addFunc"
            >

        </Button>
        <Button
            android:id="@+id/btn_read"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="READ"
            android:layout_weight="1"
            android:onClick="readFunc"
            >

        </Button>

    </LinearLayout>
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:weightSum="2"

        >
        <Button
            android:id="@+id/btn_update"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="UPDATE"
            android:layout_weight="1"
            android:onClick="updateFunc"
            >
        </Button>
        <Button
            android:id="@+id/btn_delete"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="DELETE"
            android:layout_weight="1"
            android:onClick="deleteFunc"
            >
        </Button>

    </LinearLayout>

</LinearLayout>

__________________DatabaseHelper.java___________
________________________________________________
package com.example.sqliteapp;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import androidx.annotation.Nullable;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "test.db";

    private static final int DATABASE_VERSION = 1;

    private static final String TABLE_NAME = "test_table";

    private static final String ID_COLUMN = "ID";

    private static final String NAME_COLUMN = "NAME";

    private static final String MOBILE_COLUMN = "MOBILE";


    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {

        db.execSQL("create table "+TABLE_NAME+"( ID INTEGER PRIMARY KEY AUTOINCREMENT," +"NAME TEXT," +
                "MOBILE INTEGER )");

    }

    @Override
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i1) {

    }

    public boolean insertData( String name,long Mob)
    {
        SQLiteDatabase sqLiteDatabase = this.getWritableDatabase();

        ContentValues contentValues = new ContentValues();

        contentValues.put(NAME_COLUMN,name);

        contentValues.put(MOBILE_COLUMN,Mob);

        long res = sqLiteDatabase.insert(TABLE_NAME,null,contentValues);

        return res != -1;
    }

    public Cursor readData()
    {
        SQLiteDatabase sqLiteDatabase = this.getReadableDatabase();

        Cursor cursor = sqLiteDatabase.rawQuery("SELECT * FROM "+TABLE_NAME,null);

        return cursor;
    }

    public boolean updateFunc(String id, String name, long mob)
    {
        SQLiteDatabase sqLiteDatabase = this.getWritableDatabase();

        ContentValues contentValues = new ContentValues();

        contentValues.put(ID_COLUMN,id);

        contentValues.put(NAME_COLUMN,name);

        contentValues.put(MOBILE_COLUMN,mob);

        sqLiteDatabase.update(TABLE_NAME,contentValues,"ID = ?",new String[]{id});

        return true;

    }

    public Integer deleteFunc(String id)
    {
            SQLiteDatabase sqLiteDatabase = this.getWritableDatabase();

            return sqLiteDatabase.delete(TABLE_NAME,"ID = ?",new String[]{id});
    }

}
_____________________________MainActivity.java____________
package com.example.sqliteapp;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.database.Cursor;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    EditText edt_id,edt_name,edt_mob;

    Button add_btn,read_btn,update_btn,delete_btn;

    DatabaseHelper databaseHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        edt_id = findViewById(R.id.id_edt);

        edt_name = findViewById(R.id.name_edt);

        edt_mob = findViewById(R.id.mobile_edt);

        add_btn = findViewById(R.id.btn_add);

        read_btn = findViewById(R.id.btn_read);

        update_btn = findViewById(R.id.btn_update);

        delete_btn = findViewById(R.id.btn_delete);

        databaseHelper = new DatabaseHelper(this);



    }

    public void addFunc(View v)
    {
        String name = edt_name.getText().toString();
        String mob = edt_mob.getText().toString();

        boolean check = databaseHelper.insertData(name,Long.parseLong(mob));

        if(check)
        {
            Toast.makeText(this,"Data Inserted",Toast.LENGTH_LONG).show();
        }
        else
        {
            Toast.makeText(this,"Data Not Inserted",Toast.LENGTH_LONG).show();
        }

    }

    public void updateFunc(View v)
    {
        String id = edt_id.getText().toString();
        String name = edt_name.getText().toString();
        String mob = edt_mob.getText().toString();

        boolean check = databaseHelper.updateFunc(id,name,Long.parseLong(mob));

        if(check)
        {
            Toast.makeText(this,"Data Updated",Toast.LENGTH_LONG).show();
        }
        else
        {
            Toast.makeText(this,"Data Not Updated",Toast.LENGTH_LONG).show();
        }

    }

    public void deleteFunc(View v)
    {
        String id = edt_id.getText().toString();

        Integer check = databaseHelper.deleteFunc(id);

        if(check>0)
        {
            Toast.makeText(this,"Data Deleted",Toast.LENGTH_LONG).show();
        }
        else
        {
            Toast.makeText(this,"Data Not Deleted",Toast.LENGTH_LONG).show();
        }

    }

    public void readFunc(View v)
    {
        Cursor res = databaseHelper.readData();

        if(res.getCount() == 0)
        {
            showMessage("Error","Nothing Found!");
        }
        else
        {
            StringBuffer stringBuffer = new StringBuffer();
            while (res.moveToNext())
            {
                stringBuffer.append("ID"+res.getString(0)+"\n");
                stringBuffer.append("NAME"+res.getString(1)+"\n");
                stringBuffer.append("MOBILE"+res.getString(2)+"\n");

            }
            showMessage("Data",stringBuffer.toString());

        }
    }

    private void showMessage(String error, String s)
    {
        AlertDialog.Builder alert = new AlertDialog.Builder(this);
        alert.setTitle(error);
        alert.setMessage(s);
        alert.setCancelable(true);
        alert.show();
        //alert.setPositiveButton()
    }
}

	''')
def DemoBluetooth():
	print('''
	_______________MainActivity.java_____________
	package com.example.demobluetooth;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    Button on,off;

    BluetoothAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        on = findViewById(R.id.on_btn);

        off = findViewById(R.id.off_btn);

        adapter = BluetoothAdapter.getDefaultAdapter();

        on.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!adapter.isEnabled())
                {
                    Intent i = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);

                    startActivityForResult(i,0);

                    Toast.makeText(MainActivity.this,"Bluetooth Enabled",Toast.LENGTH_LONG).show();
                }
                else
                {
                    Toast.makeText(MainActivity.this,"Bluetooth Already Enabled",Toast.LENGTH_LONG).show();
                }
            }


        });

        off.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                adapter.disable();

                Toast.makeText(MainActivity.this,"Bluetooth Disabled",Toast.LENGTH_LONG).show();
            }
        });
    }

}



_____________________AndroidManifest.xml_______________
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.demobluetooth">

    <uses-permission android:name="android.permission.BLUETOOTH"/>

    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
______________________________activity_main.xml____________________

<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.demobluetooth">

    <uses-permission android:name="android.permission.BLUETOOTH"/>

    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
	''')
def DemoPaint():
	print('''
	__________________________MainActivity.JAVA_______________
	package com.example.paintapp;

import androidx.appcompat.app.AppCompatActivity;
import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.BitmapDrawable;
import android.widget.ImageView;

import android.os.Bundle;

import com.example.paintapp.R;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Bitmap bg =Bitmap.createBitmap(720,1280,Bitmap.Config.ARGB_8888);
        ImageView i = (ImageView) findViewById(R.id.imageView);
        i.setBackgroundDrawable(new BitmapDrawable(bg));
        Canvas canvas = new Canvas(bg);
        //Creating the Paint Object and set its color &amp; TextSize
        Paint paint = new Paint();
        paint.setColor(Color.BLUE);
        paint.setTextSize(50);
        //To draw a Rectangle
        canvas.drawText("Rectangle", 420, 150, paint);
        canvas.drawRect(400, 200, 650, 700, paint);
        //To draw a Circle
        canvas.drawText("Circle", 120, 150, paint);
        canvas.drawCircle(200, 350, 150, paint);
        //To draw a Square
        canvas.drawText("Square", 120, 800, paint);
        canvas.drawRect(50, 850, 350, 1150, paint);
        //To draw a Line
        canvas.drawText("Line", 480, 800, paint);
        canvas.drawLine(520, 850, 520, 1150, paint);

    }
}

______________________________activity_main.xml___________
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"

        />

</RelativeLayout>
	''')
def DemoCalc():
	print('''
	________________________MainActivity.java_________
	package com.example.democalc;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity
{

    EditText num1,num2;
    TextView result;
    Button add,sub,mul,div;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        num1 = findViewById(R.id.edt1);
        num2 = findViewById(R.id.edt2);
        result = findViewById(R.id.res);
        add = findViewById(R.id.bt1);
        sub = findViewById(R.id.bt2);
        mul = findViewById(R.id.bt3);
        div = findViewById(R.id.bt4);

        add.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String ip1 = num1.getText().toString();
                String ip2 = num2.getText().toString();

                Double d1 = Double.parseDouble(ip1);
                Double d2 = Double.parseDouble(ip2);
                Double res = d1 + d2;
                result.setText(res.toString()); //result.setText(""+res);
            }
        });

        sub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String ip1 = num1.getText().toString();
                String ip2 = num2.getText().toString();

                Double d1 = Double.parseDouble(ip1);
                Double d2 = Double.parseDouble(ip2);
                Double res = d1 - d2;
                result.setText(res.toString()); //result.setText(""+res);
            }
        });
        mul.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String ip1 = num1.getText().toString();
                String ip2 = num2.getText().toString();

                Double d1 = Double.parseDouble(ip1);
                Double d2 = Double.parseDouble(ip2);
                Double res = d1 * d2;
                result.setText(res.toString()); //result.setText(""+res);
            }
        });

        div.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String ip1 = num1.getText().toString();
                String ip2 = num2.getText().toString();

                Double d1 = Double.parseDouble(ip1);
                Double d2 = Double.parseDouble(ip2);
                Double res = d1 / d2;
                result.setText(res.toString()); //result.setText(""+res);
            }
        });
    }
}
_______________________________activity_main.xml__________________
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout

    android:layout_width="match_parent"
    android:layout_height="match_parent"
    xmlns:tool="http://schemas.android.com/tools"
    tool:context=".MainActivity"
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical">


    <EditText
        android:id="@+id/edt1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="20dp"
        android:hint="Enter number 1"
        android:padding="20dp"
        android:inputType="numberDecimal"
        />
    <EditText
        android:id="@+id/edt2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="20dp"
        android:hint="Enter number 1"
        android:padding="20dp"
        android:inputType="numberDecimal"
        />

    <TextView
        android:id="@+id/res"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Result Here..."
        android:textSize="30sp"
        android:layout_gravity="center"

        />
<LinearLayout

    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal"
     android:gravity="center">
    <Button
        android:id="@+id/bt1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="+"
        android:textSize="25sp"
        android:textColor="#ffffff"
        android:background="#000000"
        />
    <Button
        android:id="@+id/bt2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="-"
        android:textSize="25sp"
        android:textColor="#ffffff"
        android:background="#000000"
        />
    <Button
        android:id="@+id/bt3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="*"
        android:textSize="25sp"
        android:textColor="#ffffff"
        android:background="#000000"
        />
    <Button
        android:id="@+id/bt4"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="/"
        android:textSize="25sp"
        android:textColor="#ffffff"
        android:background="#000000"
        />

</LinearLayout>
</LinearLayout>
	''')
