package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TabHost;

/**
 * Created by Ranjan on 01-09-2015.
 */
public class OutSanding_View extends TabActivity {

    TabHost tabHost;


    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.outsanding_view);

        tabHost = (TabHost) findViewById(android.R.id.tabhost);



        // OutStanding tab
        Intent intentOutStanding = new Intent().setClass(this, OutStanding_Child_View.class);
        TabHost.TabSpec tabSpecOutStanding = tabHost.newTabSpec("Outstanding");
        tabSpecOutStanding.setIndicator("Outstanding");
        tabSpecOutStanding.setContent(intentOutStanding);
        //Order Do Details
        Intent intentDdetails = new Intent().setClass(this, Order_View.class);
        TabHost.TabSpec tabSpecDdetails = tabHost.newTabSpec("DO Details");
        tabSpecDdetails.setIndicator("DO Details");
        tabSpecDdetails.setContent(intentDdetails);


        // add all tabs


        tabHost.addTab(tabSpecOutStanding);
        tabHost.addTab(tabSpecDdetails);



        //set Windows tab as default (zero based)
        tabHost.setCurrentTab(0);
    }
}
