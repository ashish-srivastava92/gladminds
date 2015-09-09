package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TabHost;
import android.widget.TextView;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Toast;

import java.math.BigInteger;

/**
 * Created by Ranjan on 22-08-2015.
 */
public class Job_details_view extends AppCompatActivity implements OnClickListener {


    TextView tv_des1,tv_des2,tv_customer1,tv_customer2,tv_site1,tv_site2,tv_eqip1,tv_equip2,tv_add1,tv_add2,tv_contact1,tv_contact2;
    TextView tv_ph1,tv_ph2,tv_mob1,tv_mob2,tv_email1,tv_email2,tv_num1,tv_num2,tv_technician1,tv_technician2,tv_jm1,tv_jm2;
    ImageView imv_ph,imv_mob,imv_email,imv_navig;
    LinearLayout ll_ph_call, ll_mobile_call, ll_email,ll_navig_image,ll_navig;
    private static final int i=0;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.demo_layout);

        imv_ph = (ImageView) findViewById(R.id.imv_ph_nm);
        imv_mob = (ImageView) findViewById(R.id.imv_mobile);
        imv_email = (ImageView) findViewById(R.id.imv_email_symbol_input);
        imv_navig = (ImageView) findViewById(R.id.imv_navig);



        tv_des1 = (TextView) findViewById(R.id.tv_hr_operation1);
        tv_des2 = (TextView) findViewById(R.id.tv_opn_time1);
        tv_customer1 = (TextView) findViewById(R.id.tv_hr_operation2);
        tv_customer2 = (TextView) findViewById(R.id.tv_opn_time2);
        tv_site1 = (TextView) findViewById(R.id.tv_hr_operation4);
        tv_site2 = (TextView) findViewById(R.id.tv_opn_time4);
        tv_eqip1 = (TextView) findViewById(R.id.tv_hr_operation5);
        tv_equip2 = (TextView) findViewById(R.id.tv_opn_time5);


        tv_contact1 = (TextView) findViewById(R.id.tv_hr_operation7);
        tv_contact2 = (TextView) findViewById(R.id.tv_opn_time7);

        tv_ph1 = (TextView) findViewById(R.id.tv_ph_call);
        tv_ph2 = (TextView) findViewById(R.id.tv_ph_number);
        tv_mob1 = (TextView) findViewById(R.id.tv_mobile_call);
        tv_mob2 = (TextView) findViewById(R.id.tv_mobile_number);


        tv_email1 = (TextView) findViewById(R.id.tv_email);
        tv_email2 = (TextView) findViewById(R.id.tv_email_id);
        tv_num1 = (TextView) findViewById(R.id.tv_hr_operation11);
        tv_num2 = (TextView) findViewById(R.id.tv_opn_time11);

        tv_technician1 = (TextView) findViewById(R.id.tv_sub11_12);
        tv_technician2 = (TextView) findViewById(R.id.tv_sub12_12);

        ll_ph_call = (LinearLayout)findViewById(R.id.ll_ph_call);
        ll_mobile_call = (LinearLayout)findViewById(R.id.ll_mobile);
        ll_email = (LinearLayout)findViewById(R.id.ll_Info_email);
        ll_navig_image=(LinearLayout)findViewById(R.id.ll_navig_image);
        ll_navig=(LinearLayout)findViewById(R.id.ll_navig);





        imv_ph.setOnClickListener(this);
        imv_navig.setOnClickListener(this);
        imv_mob.setOnClickListener(this);
        imv_email.setOnClickListener(this);
        ll_ph_call.setOnClickListener(this);
        ll_mobile_call.setOnClickListener(this);
        ll_email.setOnClickListener(this);
        ll_navig_image.setOnClickListener(this);
        ll_navig.setOnClickListener(this);




    }

    @Override
    public void onClick(View v)
    {
        switch(v.getId())
        {


            case R.id.imv_ph_nm:

                onMakeCall();

                break;

            case R.id.imv_mobile:


                onMakeCall();

                break;

            case R.id.imv_navig:
                Intent myIntent = new Intent(getApplicationContext(), Get_directions.class);
                startActivity(myIntent);

                break;

            case R.id.ll_navig:
                Intent myIntent_get = new Intent(getApplicationContext(), Get_directions.class);
                startActivity(myIntent_get);

                break;

            case R.id.imv_email_symbol_input:
                String email=tv_email2.getText().toString();
                onEmail_Send(email);
                break;



            //Layout call part
            case R.id.ll_ph_call: {

                onMakeCall();

            }
                break;

            case R.id.ll_mobile: {


                onMakeCall();
            }
                break;

            case R.id.ll_Info_email:
                String email_send=tv_email2.getText().toString();
                onEmail_Send(email_send);

                break;

            case R.id.ll_navig_image:

                Intent myIntent_direction = new Intent(getApplicationContext(), Get_directions.class);
                startActivity(myIntent_direction);
                break;

            default:
                break;
        }
    }

    //	<<	Alert Message for Phone>>
    public void onMakeCall( ) {
        final BigInteger ph=new BigInteger("9818690998");
        AlertDialog.Builder builder = new AlertDialog.Builder(Job_details_view.this);
        builder.setMessage("Calling Number "+""+ph +
                "\n"+"Do you want to continue")
                .setCancelable(false)
                .setPositiveButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                    }
                })
                .setNegativeButton("Continue", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
//	       			<<<	To make call, exit from the main application	>>>
                        try {
                            Intent callIntent = new Intent(Intent.ACTION_CALL);
                            callIntent.setData(Uri.parse("tel:" + ph));
                            startActivity(callIntent);
                        } catch (ActivityNotFoundException e) {
                            Toast toast = Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT);
                            toast.show();
                        }

                    }
                });
        AlertDialog alert = builder.create();
        alert.show();

    }


    public void onEmail_Send(String email ){


        String[] TO = {email};
        Intent emailIntent = new Intent(android.content.Intent.ACTION_SEND);
        emailIntent.setType("plain/text");
        emailIntent.putExtra(Intent.EXTRA_EMAIL, TO);
        emailIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, " Feedback from "+ getResources().getString(R.string.app_name));
        emailIntent.putExtra(android.content.Intent.EXTRA_TEXT,"");
        startActivity(Intent.createChooser(emailIntent, "Email:"));

    }


    public String getDeviceName() {
        String manufacturer = Build.MANUFACTURER;
        String model = Build.MODEL;
        if (model.startsWith(manufacturer)) {
            return capitalize(model);
        } else {
            return capitalize(manufacturer) + " " + model;
        }
    }


    private String capitalize(String s) {
        if (s == null || s.length() == 0) {
            return "";
        }
        char first = s.charAt(0);
        if (Character.isUpperCase(first)) {
            return s;
        } else {
            return Character.toUpperCase(first) + s.substring(1);
        }
    }





}
