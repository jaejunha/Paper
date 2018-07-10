package kr.ac.postech.dreamline91.client;

import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import com.google.android.exoplayer2.ExoPlayerFactory;
import com.google.android.exoplayer2.SimpleExoPlayer;
import com.google.android.exoplayer2.extractor.DefaultExtractorsFactory;
import com.google.android.exoplayer2.source.ExtractorMediaSource;
import com.google.android.exoplayer2.source.MediaSource;
import com.google.android.exoplayer2.trackselection.AdaptiveTrackSelection;
import com.google.android.exoplayer2.trackselection.DefaultTrackSelector;
import com.google.android.exoplayer2.trackselection.TrackSelection;
import com.google.android.exoplayer2.ui.SimpleExoPlayerView;
import com.google.android.exoplayer2.upstream.BandwidthMeter;
import com.google.android.exoplayer2.upstream.DataSource;
import com.google.android.exoplayer2.upstream.DefaultBandwidthMeter;
import com.google.android.exoplayer2.upstream.DefaultDataSourceFactory;
import com.google.android.exoplayer2.upstream.TransferListener;
import com.google.android.exoplayer2.util.Util;

public class MainActivity extends AppCompatActivity {

    private SimpleExoPlayerView exoView;
    private SimpleExoPlayer exo;

    private BandwidthMeter meter;
    private DefaultTrackSelector selector;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        meter = new DefaultBandwidthMeter();

        exoView = findViewById(R.id.exoView);
        exoView.requestFocus();

        selector = new DefaultTrackSelector(new AdaptiveTrackSelection.Factory(meter));
        //selector.setParameters(selector.getParameters().withMaxVideoBitrate(1));
        exo = ExoPlayerFactory.newSimpleInstance(this, selector);
        exoView.setPlayer(exo);
        exo.setPlayWhenReady(true);

        exo.prepare(new ExtractorMediaSource(Uri.parse("http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"),
                new DefaultDataSourceFactory(this, Util.getUserAgent(this, "Client"),
                        (TransferListener<? super DataSource>) meter), new DefaultExtractorsFactory(), null, null));


        new Thread() {
            public void run() {
                try {
                    while(true) {
                        Log.d("estimation", "estimation: " + meter.getBitrateEstimate());
                        Log.d("estimation", "maxBitrate: " + selector.getParameters().maxVideoBitrate);
                        sleep(1000);
                    }
                }catch(Exception e){

                }
            }
        }.start();
    }
}
