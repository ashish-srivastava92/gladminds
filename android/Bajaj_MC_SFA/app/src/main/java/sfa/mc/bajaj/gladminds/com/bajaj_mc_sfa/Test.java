package sfa.mc.bajaj.gladminds.com.bajaj_mc_sfa;

/**
 * Created by Ranjan on 03-09-2015.
 */



import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;



import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.provider.Settings;
import android.support.v7.app.AlertDialog;
import android.text.TextUtils;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;


public class Test extends Activity{

    //URL to get JSON Array
    private static String url = "http://192.168.0.50:8000/get_retailers/dsr_id/1/";

    //JSON Node Names
    private static final String VTYPE = "Type";
    private static final String VCOLOR = "Color";
    private static final String FUEL = "Fuel";
    private static final String TREAD = "Tread";

    static String[] F_NAME, L_NAME;
    TextView tv;
    ListView retails_details;






    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.check);

        retails_details=(ListView) findViewById(R.id.lstContacts);
        retails_details.setItemsCanFocus(true);



        // we will using AsyncTask during parsing
        new AsyncTaskParseJson().execute();

    }



    public class AsyncTaskParseJson extends AsyncTask<String, String, String> {

        private ProgressDialog dialog;

        final String TAG = "AsyncTaskParseJson.java";

        // set your json string url here
        //String yourJsonStringUrl = "http://demo.codeofaninja.com/tutorials/json-example-with-php/index.php";

        // contacts JSONArray
        JSONArray dataJsonArr = null;
        JSONArray dataJsonArr_iner = null;
        JSONObject jsonObject=null;




        @Override
        protected String doInBackground(String... arg0) {

            try {



                JsonParser jParser = new JsonParser();

               dataJsonArr = jParser.getJSONFromUrl_arrayData(url);
                F_NAME= new String[dataJsonArr.length()];
                L_NAME= new String[dataJsonArr.length()];



                // loop through all users
                for (int i = 0; i < dataJsonArr.length(); i++) {

                    JSONObject c = dataJsonArr.getJSONObject(i);

                    // Storing each json item in variable
                    String firstname = c.getString("retailer_name");
                    String lastname = c.getString("retailer_mobile");





                    // show the values in our logcat
                    Log.e(TAG, "retailer_name: " + firstname
                            + ", retailer_mobile: " + lastname
                            );
                    F_NAME[i]=firstname;
                    L_NAME[i]=lastname;


                }

            } catch (JSONException e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String strFromDoInBg) {

            ListImageAdapter retails_adapter = new ListImageAdapter(Test.this,F_NAME,L_NAME);
            retails_details.setAdapter(retails_adapter);


        }
    }






}
