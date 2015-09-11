package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;

/**
 * Created by RJ on 8/14/2015.
 */


import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;

import android.net.Uri;

import android.os.Bundle;

import android.support.v7.app.AppCompatActivity;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;

import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import android.content.DialogInterface;

import java.math.BigInteger;


public class MenuView_Activity  extends AppCompatActivity implements View.OnClickListener  {



    TextView tv_top;
    ImageView imv_back,imv_save;
    ListView retails_details;

    static String list_content1[] = {"AMK AUTOMOBILES","S P AUTOMOBILES","PRAKASH AUTO SPARES","K L AUTO SPARES","MANI AUTOMOBILES","BAJAJ AUTOMOBILES"};
    static String list_content_second1[] = {"221133","112356","675890","453245","896756","011456"};
    static Integer ph_call[]={012345,03456,221133,112356,675890,453245};






    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.menu_activity);







        retails_details=(ListView) findViewById(R.id.retails_location_listview);
        retails_details.setItemsCanFocus(true);
        tv_top = (TextView) findViewById(R.id.tv_tittle_bar);
        imv_back=(ImageView) findViewById(R.id.iv_back);
        imv_save=(ImageView) findViewById(R.id.iv_save);
        imv_back.setOnClickListener(this);
        imv_save.setOnClickListener(this);




        LvAdapter retails_adapter = new LvAdapter(this, list_content1,ph_call,list_content_second1);
        retails_details.setAdapter(retails_adapter);

        retails_details.setOnItemClickListener((new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
                int itemPosition     = position;
                Intent myIntent = new Intent(getApplicationContext(), Retailer_Tab_View.class);
                myIntent.putExtra("listPosition", itemPosition);
                startActivity(myIntent);
            }
        }));

    }


    @Override
    public void onClick(View v) {

        switch (v.getId()) {


            case R.id.iv_back:{
                Intent myIntent = new Intent(getApplicationContext(),MainViewActivity.class);
                startActivity(myIntent);
                overridePendingTransition(R.anim.push_up_in, R.anim.push_up_out);

                //finish();
            }
                break;

            case R.id.iv_save:

                break;

            default:
                break;
        }

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main_view, menu);
        return true;
    }


     public class LvAdapter extends BaseAdapter {

            Activity context;
            String get_retails_name[];
            String get_retails_contact_number[];
            Integer[]calling;



        public LvAdapter(Activity context, String[] retails_name1,Integer[] ph_call,String[]retails_contact1 ) {
            super();
            this.context = context;
            this.get_retails_name = retails_name1;
            this.get_retails_contact_number = retails_contact1;
            this.calling=ph_call;

        }

        public int getCount() {
            return get_retails_name.length;
        }

        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return 0;
        }

        private class ViewHolder {
            TextView tv_field_retails_nm,tv_field_retails_number;
            ImageView img_ph_nm,img_mobile_nm,img_email;

        }

        public View getView(int position, View convertView, ViewGroup parent)
        {

            // TODO Auto-generated method stub
            final ViewHolder holder;
            LayoutInflater inflater =  context.getLayoutInflater();

            if (convertView == null)
            {



//			Typeface font = Typeface.createFromAsset(context.getAssets(), "LinotypeZapfino One.ttf");
                convertView = inflater.inflate(R.layout.retail_list_item, null);
                holder = new ViewHolder();
                holder.tv_field_retails_nm = (TextView) convertView.findViewById(R.id.tv_retail_name);
                holder.tv_field_retails_number = (TextView) convertView.findViewById(R.id.tv_retail_contact);

                holder.img_ph_nm = (ImageView) convertView.findViewById(R.id.imv_ph_call);
                holder.img_mobile_nm = (ImageView) convertView.findViewById(R.id.imv_mobile_call);
                holder.img_email = (ImageView) convertView.findViewById(R.id.imv_email);

//			holder.tv_field.setTypeface(font);

                convertView.setTag(holder);
            }
            else
            {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.tv_field_retails_nm.setText(get_retails_name[position]);
            holder.tv_field_retails_number.setText(get_retails_contact_number[position]);


            holder.img_ph_nm.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (calling.length > 0) {
                        onMakeCall(calling[0]);
                    } else {
                        Toast toast = Toast.makeText(context, "Ph number not available", Toast.LENGTH_SHORT);
                        toast.show();
                    }
                }
            });

            holder.img_mobile_nm.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (calling.length > 0) {
                        onMakeCall(calling[0]);
                    } else {
                        Toast toast = Toast.makeText(context, "Mobile number not available", Toast.LENGTH_SHORT);
                        toast.show();
                    }
                }
            });


            holder.img_email.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    String email = "rjhazarika712@gmail.com";
                    onEmail_Send(email);
                }
            });


            return convertView;
        }

         //	<<	Alert Message for Phone>>
         public void onMakeCall(final int phn_number) {
             AlertDialog.Builder builder = new AlertDialog.Builder(context);
             builder.setMessage("By making call, you will be exiting the application."+
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
                                 final BigInteger ph_call = BigInteger.valueOf(phn_number);
                                 ;
                                 Intent callIntent = new Intent(Intent.ACTION_CALL);
                                 callIntent.setData(Uri.parse("tel:" + ph_call));
                                 context.startActivity(callIntent);
                             } catch (ActivityNotFoundException e) {
                                 Toast toast = Toast.makeText(context, e.toString(), Toast.LENGTH_SHORT);
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
             emailIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, " DSR Report from "+ getResources().getString(R.string.app_name));
             emailIntent.putExtra(android.content.Intent.EXTRA_TEXT, "");
             startActivity(Intent.createChooser(emailIntent, "Email:"));

         }



     }




}
