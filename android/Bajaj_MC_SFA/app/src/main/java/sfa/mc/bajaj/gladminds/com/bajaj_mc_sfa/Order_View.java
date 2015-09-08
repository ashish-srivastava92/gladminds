package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ScrollView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Gallery.LayoutParams;
import android.widget.Toast;
import android.widget.ViewAnimator;

import java.io.File;
import java.text.DecimalFormat;

/**
 * Created by Ranjan on 18-08-2015.
 */
public class Order_View extends FragmentActivity implements android.view.View.OnClickListener {



    private TableLayout table,table_tittle;
    TextView tv_top,tv_rnm,tv_total,tv_total_amount,tv_item,tv_quantity,tv_price;
    ImageView sig,imv_save;
    final int CHECK_ET_ID = 982301;
    final int CHECK_TV_ID = 882301;
    final int CHECK_BTN_ID = 782301;
    final int CHECK_TV2_ID = 682301;
    private int ids_et[];
    private int ids_tv[];
    private int ids_btn[];
    private int total_data[]={};
    static int total=0,sub_total=0;
    private ViewAnimator viewAnimator, btnAnimator;

    private String list_item_content[] = {"976DEMOPART1","912DEMOPART2","940DEMOPART3"};
    private String list_item_price[] = {"150","200","120"};
    private Integer list_price[] = {10,20,10};

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.filp_view);
        table = (TableLayout) findViewById(R.id.tbl_order);
        //table_tittle = (TableLayout) findViewById(R.id.tble_tittle);
        tv_top = (TextView) findViewById(R.id.tv_tittle_bar);
        tv_rnm = (TextView) findViewById(R.id.tv_retail_name);
        tv_total = (TextView) findViewById(R.id.tv_total_text);
        tv_total_amount=(TextView)findViewById(R.id.tv_total_amount);
        tv_item = (TextView) findViewById(R.id.tv_total_order);
        sig = (ImageView) findViewById(R.id.show_my_sig);
        viewAnimator = (ViewAnimator)this.findViewById(R.id.viewFlipper);



        File imgFile1= new File("/sdcard/Philips/Customer.jpeg");
        if(imgFile1.exists()){
            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile1.getAbsolutePath());
            sig.setImageBitmap(myBitmap);

        }

        tv_item.setOnClickListener(this);


        createTableRows();


    }


    private void createTableRows() {

        table.setColumnStretchable(0, true);
        table.setColumnStretchable(1, true);
        table.setColumnStretchable(2, true);
        table.setColumnStretchable(3, true);
        table.setColumnStretchable(4, true);
        table.setColumnStretchable(5, true);
        table.setColumnStretchable(6, true);
        table.setColumnStretchable(7, true);


        ids_et = new int[list_item_content.length];
        ids_tv = new int[list_item_content.length];
        ids_btn = new int[list_item_content.length];
        total_data=new int[list_item_content.length];


         TableRow table_row_item = new TableRow(this);
         TextView tv_1_item = new TextView(this);
         TextView tv_3_item = new TextView(this);
         TextView tv_2_item = new TextView(this);
         TextView tv_4_item = new TextView(this);
         table_row_item.setLayoutParams(new LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, android.view.ViewGroup.LayoutParams.WRAP_CONTENT));
         table_row_item.setGravity(Gravity.CENTER);
         table_row_item.setPadding(0, 0, 0, 0);
         table_row_item.setBackgroundColor(Color.WHITE);

         tv_3_item.setText("QTY");
         tv_3_item.setTextColor(Color.GRAY);
         tv_3_item.setTextSize(20);
         tv_3_item.setMaxLines(2);
         tv_3_item.setBackgroundColor(Color.WHITE);
         TableRow.LayoutParams params3_item = new TableRow.LayoutParams();
         tv_3_item.setLayoutParams(params3_item);
         tv_3_item.setGravity(Gravity.CENTER);
         tv_3_item.setHeight(60);


         tv_1_item.setText("ITEMS");
         tv_1_item.setTextColor(Color.GRAY);
         tv_1_item.setTextSize(20);
         tv_1_item.setMaxLines(1);
         tv_1_item.setBackgroundColor(Color.WHITE);
         TableRow.LayoutParams params_item = new TableRow.LayoutParams();
         params_item.span = 2;
         tv_1_item.setLayoutParams(params_item);
         tv_1_item.setGravity(Gravity.CENTER);
         tv_1_item.setHeight(60);


         tv_2_item.setText("Unit Price");
         tv_2_item.setTextColor(Color.GRAY);
         tv_2_item.setTextSize(20);
         tv_2_item.setMaxLines(1);
         tv_2_item.setBackgroundColor(Color.WHITE);
         TableRow.LayoutParams params2_item = new TableRow.LayoutParams();
         tv_2_item.setLayoutParams(params2_item);
         tv_2_item.setGravity(Gravity.CENTER);
         tv_2_item.setHeight(60);

            tv_4_item.setText("Total Price");
            tv_4_item.setTextColor(Color.GRAY);
            tv_4_item.setTextSize(20);
            tv_4_item.setMaxLines(1);
            tv_4_item.setBackgroundColor(Color.WHITE);
            TableRow.LayoutParams params4_item = new TableRow.LayoutParams();
            params4_item.span=1;
            tv_4_item.setLayoutParams(params4_item);
            tv_4_item.setGravity(Gravity.CENTER);
            tv_4_item.setHeight(60);


         table_row_item.addView(tv_1_item);
         table_row_item.addView(tv_2_item);
         table_row_item.addView(tv_3_item);
         table_row_item.addView(tv_4_item);

table.addView(table_row_item, new TableLayout.LayoutParams(
android.view.ViewGroup.LayoutParams.WRAP_CONTENT, android.view.ViewGroup.LayoutParams.WRAP_CONTENT));

 /***Here table data work done  **/

        for (int i = 0; i < list_item_content.length; i++) {
            TableRow table_row = new TableRow(this);
            ScrollView sv = new ScrollView(this);
            TextView items_menu = new TextView(this);
            final EditText et = new EditText(this);
            TextView total_price = new TextView(this);
            TextView txt_delete = new TextView(this);
            //Button btn_delete = new Button(this);

            TextView Total_price_new=new TextView(this);

            et.setId(i + CHECK_ET_ID);
            ids_et[i] = i + CHECK_ET_ID;
            total_price.setId(i + CHECK_TV_ID);
            ids_tv[i] = i + CHECK_TV_ID;
            Total_price_new.setId(i + CHECK_TV2_ID);
            ids_btn[i] = i + CHECK_TV2_ID;


            //Toast.makeText(Order_View.this,"test1"+ids_btn[i], Toast.LENGTH_SHORT).show();

            table_row.setLayoutParams(new LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
            table_row.setGravity(Gravity.CENTER);

            table_row.setBackgroundColor(Color.WHITE);

            et.setText("" + list_price[i]);
            et.setInputType(InputType.TYPE_CLASS_NUMBER);
            TableRow.LayoutParams params2 = new TableRow.LayoutParams();
            et.setLayoutParams(params2);
            et.setPadding(0, 10, 10, 10);
            et.setWidth(50);
            et.setEnabled(false);
            et.setGravity(Gravity.CENTER);
            et.setHeight(80);


            items_menu.setText(list_item_content[i]);
            items_menu.setTextColor(Color.BLACK);
            items_menu.setTextSize(17);
            items_menu.setMaxLines(5);
            items_menu.setBackgroundColor(Color.WHITE);
            items_menu.setGravity(Gravity.CENTER);

            sv.setBackgroundColor(Color.WHITE);
            TableRow.LayoutParams params = new TableRow.LayoutParams();
            sv.setLayoutParams(params);
            sv.addView(items_menu, new ScrollView.LayoutParams(
            android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 100));



            total_price.setText("" + Float.parseFloat(list_item_price[i]));
//	    		tv_2.setText(MainActivity.MENU_PRICE[selectedItems[i]]);
            total_price.setTextColor(Color.BLACK);
            total_price.setTextSize(16);
            total_price.setBackgroundColor(Color.WHITE);
            TableRow.LayoutParams params3 = new TableRow.LayoutParams();

            total_price.setLayoutParams(params3);
            total_price.setGravity(Gravity.CENTER);
            total_price.setHeight(100);

            int qty = list_price[i];
            float price = qty * Float.parseFloat(list_item_price[i] );
            total_data[i] =  (int) price;
            Total_price_new.setText(new DecimalFormat("##.##").format(price));
//	    		tv_2.setText(MainActivity.MENU_PRICE[selectedItems[i]]);
            Total_price_new.setTextColor(Color.BLACK);
            Total_price_new.setTextSize(16);
            Total_price_new.setBackgroundColor(Color.WHITE);
            TableRow.LayoutParams params4 = new TableRow.LayoutParams();
            Total_price_new.setLayoutParams(params3);
            Total_price_new.setGravity(Gravity.CENTER);
            Total_price_new.setHeight(100);



            table.addView(table_row, new TableLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            //Init_field_Calculate();



            txt_delete.setText("x");
            //tv_2.setText(MainActivity.MENU_PRICE[selectedItems[i]]);
            txt_delete.setTextColor(Color.RED);
            txt_delete.setTextSize(30);
            txt_delete.setBackgroundColor(Color.WHITE);
            TableRow.LayoutParams params_delte = new TableRow.LayoutParams();
            txt_delete.setLayoutParams(params_delte);
            txt_delete.setGravity(Gravity.CENTER);
            txt_delete.setHeight(70);

            table_row.addView(txt_delete);
            table_row.addView(sv);
            table_row.addView(total_price);
            table_row.addView(et);
            table_row.addView(Total_price_new);



            Init_field_Calculate();


            et.addTextChangedListener(new TextWatcher() {
                @Override
                public void afterTextChanged(Editable s) {
                    fieldCalculate();
                }

                @Override
                public void beforeTextChanged(CharSequence s,
                                              int start, int count, int after) {
                }

                @Override
                public void onTextChanged(CharSequence s,
                                          int start, int before, int count) {
                }
            });




        }


    }



    @Override
    public void onClick(View v)
    {

        switch(v.getId())
        {

            case R.id.tv_total_order:
                for(int i=0; ids_et.length>i; i++)
                    {
                    EditText ET = (EditText)findViewById(ids_et[i]);
                    ET.setEnabled(true);
                    }

                Intent myIntent = new Intent(getApplicationContext(), Add_item_view.class);
                startActivity(myIntent);

                //AnimationFactory.flipTransition(viewAnimator, AnimationFactory.FlipDirection.LEFT_RIGHT);
                break;

            default:
                break;
        }

    }

    private void Init_field_Calculate() {
      int init_total=0;

      for (int j = 0; j < ids_et.length; j++)
        {
            init_total=init_total+total_data[j];

        }

    int total_s = init_total;

     tv_total_amount.setText(new DecimalFormat("##.##").format(total_s));
    }


    private void fieldCalculate() {

        total = sub_total = 0;
        int show[]=new int[ids_et.length];
        int t=0;

        for (int j = 0; j < ids_et.length; j++) {
            TextView TV = (TextView) findViewById(ids_btn[j]);
            EditText ET = (EditText) findViewById(ids_et[j]);

            String text = ET.getText().toString();

            if (!text.equals("") || !text.equals("0")) {
                int qty = 1;
                try {
                    qty = Integer.parseInt(text);

                } catch (Exception e) {
                    qty = 0;
                }

                float price = qty * Float.parseFloat(list_item_price[j]);
                sub_total = sub_total + (int) price;
                TV.setText(new DecimalFormat("##.##").format(price));
                show[j] =  sub_total;
            }
            total = t+show[j];

        }


        tv_total_amount.setText(new DecimalFormat("##.##").format(total));


    }


}



