# RedVTY
# Copyright (C) 2019  Red_M ( http://bitbucket.com/Red_M )

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import pyte
import multiprocessing
import redexpect


class RedVTY(redexpect.RedExpect):
    def __init__(self, *args, columns=80, rows=24, **kwargs):
        super().__init__(*args,**kwargs)
        self.columns = columns
        self.rows = rows
        self._stream_lock = multiprocessing.Lock()
        self.stream_init()

    def stream_init(self):
        self.screen = pyte.Screen(self.columns,self.rows)
        self.stream = pyte.ByteStream(self.screen)

    def out_feed(self,data):
        with self._stream_lock:
            self.stream.feed(data)


