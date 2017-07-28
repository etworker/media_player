# media_player

simple media player based on opencv
support web camera / video file / live url
press ESC key to quit playing

## usage example

- play with local camera

```python media_player.py --uri 0```

- play with local video file test.mp4, display in full screen

```python media_player.py --uri test.mp4 --full```

- play with live url rtmp://192.168.0.191:1935/live1/

```python media_player.py --uri rtmp://192.168.0.191:1935/live1/```